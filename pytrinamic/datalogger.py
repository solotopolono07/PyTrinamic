################################################################################
# Copyright © 2025 Analog Devices Inc. All Rights Reserved.
# This software is proprietary to Analog Devices, Inc. and its licensors.
################################################################################

"""User interface for the RAMDebug feature of some ADI Trinamic products

Improvements/Todo:
* Add an optional explode mode that will unpack all fields of a register in the logs.
* Add a way to call download_logs() without waiting for the logging to be done.
* Add parameters to download_logs() that allow to download only a part of the logs.
* Add timeouts to wait_till_done() and wait_for_trigger().
"""

from __future__ import annotations
from typing import Union, List, Dict
from dataclasses import dataclass
from enum import Enum, auto
import decimal
import math

from pytrinamic.rd import Rd
from pytrinamic.modules.tmcl_module import ParameterGroup, Parameter
from pytrinamic.ic.tmc_ic import Register, Field
from pytrinamic.helpers import to_signed_32


class DataLoggerConfigError(Exception):
    pass


class DataLogger:

    @dataclass
    class Info:
        base_frequency_hz: int
        sample_buffer_length: int
        number_of_channels: int

    class DataType:
        def __init__(self):
            self.reuse_obj = None

    class DataTypeAp(DataType):
        def __init__(self, index, axis=0, signed=False):
            super().__init__()
            self.index = index
            self.axis = axis
            self.signed = signed

        @classmethod
        def from_parameter(cls, parameter: Parameter, axis: int = 0) -> DataLogger.DataTypeAp:
            return cls(
                index=parameter.index,
                axis=axis,
                signed=(parameter.datatype==Parameter.Datatype.SIGNED),
            )
        
        def __eq__(self, other):
            if not isinstance(other, DataLogger.DataTypeAp):
                return False
            if self.index == other.index and self.axis == other.axis:
                return True
            else:
                return False

    class DataTypeGp(DataType):
        def __init__(self, index, bank=0, signed=False):
            super().__init__()
            self.index = index
            self.bank = bank
            self.signed = signed

        @classmethod
        def from_parameter(cls, parameter: Parameter) -> DataLogger.DataTypeGp:
            return cls(
                index=parameter.index,
                bank=parameter.block,
                signed=(parameter.datatype==Parameter.Datatype.SIGNED),
            )
        
        def __eq__(self, other):
            if not isinstance(other, DataLogger.DataTypeGp):
                return False
            if self.index == other.index and self.bank == other.bank:
                return True
            else:
                return False
    
    class DataTypeRegister(DataType):
        def __init__(self, block, channel, address, signed=False):
            super().__init__()
            self.block = block
            self.channel = channel
            self.address = address
            self.signed = signed

        @classmethod
        def from_register(cls, register: Register) -> DataLogger.DataTypeRegister:
            return cls(
                block=register.parent.block,
                channel=register.parent.channel,
                address=register.address,
                signed=register.signed,
            )
        
        def __eq__(self, other):
            if not isinstance(other, DataLogger.DataTypeRegister):
                return False
            if all([
                self.block == other.block,
                self.channel == other.channel,
                self.address == other.address,
            ]):
                return True
            else:
                return False
        
    class DataTypeField(DataType):
        def __init__(self, block, field, channel, signed=False):
            super().__init__()
            self.block = block
            self.channel = channel
            self.address = field[0]
            self.mask = field[1]
            self.shift = field[2]
            self.signed = signed

        @classmethod
        def from_field(cls, field: Field) -> DataLogger.DataTypeField:
            return cls(
                block=field.parent.parent.block,
                field=(field.parent.address, field.mask, field.shift),
                channel=field.parent.parent.channel,
                signed=field.signed,
            )

        def get(self, register_value) -> int:
            value = (register_value & self.mask) >> self.shift
            if self.signed:
                base_mask = self.mask >> self.shift
                sign_mask = base_mask & (~base_mask >> 1)
                value = (value ^ sign_mask) - sign_mask
            return value
        
    class TriggerEdge(Enum):
        RISING = auto()
        FALLING = auto()
        BOTH = auto()

    @dataclass
    class Log:
        rate_hz: float
        period_s: float
        time_vector: list
        data: Dict[str, DataLogger.LogData]

    @dataclass
    class LogData:
        samples: list
        request_object: None

    @dataclass
    class Config:
        down_sampling_factor: int
        samples_per_channel: int
        log_data: dict
        _get_base_frequency_hz: None

        def set_sample_rate(self, rate_hz: float, *, round_down=False) -> float:
            """
            Sets the sampling rate of the data logger.

            If round_down is set, this will round down to the nearest valid
            frequency. Otherwise, it will a DataLoggerConfigError for any
            frequency that cannot be exactly represented.
            """
            if self.down_sampling_factor is not None:
                raise DataLoggerConfigError("The `config.down_sampling_factor` is already set!")
            base_frequency_hz = self._get_base_frequency_hz()
            expected_down_sampling_factor = base_frequency_hz/rate_hz
            if expected_down_sampling_factor.is_integer() or round_down:
                # Note: Rounding down the frequency means rounding up the downsampling
                self.down_sampling_factor = math.ceil(expected_down_sampling_factor)
            else:
                possibilities = []
                for i in range(1, 1000):
                    freq = base_frequency_hz/i
                    if decimal.Decimal(freq).as_tuple().exponent < -4:
                        continue
                    possibilities.append((i, freq))
                    if len(possibilities) > 10:
                        break
                msg = f"The `rate_hz` must be a divisor of the base frequency {base_frequency_hz} Hz! Good values would be:\n" \
                    f"  Frequency Hz | down_sampling_factor\n" \
                    f"{f'{chr(10)}'.join([f'  {frequency:12} | {factor:3}' for factor, frequency in possibilities])}"
                raise DataLoggerConfigError(msg)

    @dataclass
    class _RequestEntry:
        name: str
        datatype: DataLogger.DataType
        request_object: None

    def __init__(self, connection, module_id=1):
        self.rd = Rd(connection, module_id)
        self.config = DataLogger.Config(
            down_sampling_factor=None,
            samples_per_channel=0,
            log_data=None,
            _get_base_frequency_hz=self._get_base_frequency_hz,
        )
        self.log = DataLogger.Log(rate_hz=0, period_s=0, time_vector=[], data={})
        self._log_data = None
        self._effectively_log_data = None
        self._info = None
        self._down_sampling_factor = 1
        self._channels_used_count = 0
        self._total_number_of_samples = 0
        self._download_is_done = True
        self._download_offset = 0
        self._downloaded_raw_data = []
        self._trigger_type = Rd.TriggerType.UNCONDITIONAL
        self._trigger_on = None
        self._trigger_threshold = None
        self._pretrigger_samples = 0

    def get_info(self) -> DataLogger.Info:
        return DataLogger.Info(
            base_frequency_hz=self.rd.get_info(Rd.Info.SAMPLING_FREQUENCY),
            sample_buffer_length=self.rd.get_info(Rd.Info.BUFFER_ELEMENTS),
            number_of_channels=self.rd.get_info(Rd.Info.MAX_CHANNELS),
        )
    
    def start_logging(self):
        self._trigger_type = Rd.TriggerType.UNCONDITIONAL
        self._activation()

    def activate_trigger(
            self,
            *,
            on_data: Union[Parameter, Register, Field, DataTypeAp, DataTypeGp, DataTypeRegister, DataTypeField],
            threshold: int,
            edge: TriggerEdge,
            pretrigger_samples: int = 0,
        ) -> None:
        
        if isinstance(on_data, (Parameter, Register, Field)):
            self._trigger_on = self._transform_to_datatype(on_data)
        else:
            self._trigger_on = on_data
        if self._trigger_on.signed:
            if edge == DataLogger.TriggerEdge.RISING:
                self._trigger_type = Rd.TriggerType.RISING_EDGE_SIGNED
            elif edge == DataLogger.TriggerEdge.FALLING:
                self._trigger_type = Rd.TriggerType.FALLING_EDGE_SIGNED
            elif edge == DataLogger.TriggerEdge.BOTH:
                self._trigger_type = Rd.TriggerType.DUAL_EDGE_SIGNED
        else:
            if edge == DataLogger.TriggerEdge.RISING:
                self._trigger_type = Rd.TriggerType.RISING_EDGE_UNSIGNED
            elif edge == DataLogger.TriggerEdge.FALLING:
                self._trigger_type = Rd.TriggerType.FALLING_EDGE_UNSIGNED
            elif edge == DataLogger.TriggerEdge.BOTH:
                self._trigger_type = Rd.TriggerType.DUAL_EDGE_UNSIGNED
        self._trigger_threshold = threshold
        self._pretrigger_samples = pretrigger_samples
        self._activation()

    def _activation(self) -> None:
        if self.config.down_sampling_factor is None:
            self._down_sampling_factor = 1
        else:
            if self.config.down_sampling_factor < 1:
                raise DataLoggerConfigError("The `config.down_sampling_factor` must be greater than 0!")
            self._down_sampling_factor = self.config.down_sampling_factor
        if self.config.samples_per_channel == 0:
            raise DataLoggerConfigError("No samples per channel specified via `config.samples_per_channel`!")
        
        if isinstance(self.config.log_data, list):
            self._log_data = []
            for x in self.config.log_data:
                dt = self._transform_to_datatype(x)
                if isinstance(x, Field):
                    self._log_data.append(self._RequestEntry(name=f"{x.parent.name}.{x.name}", datatype=dt, request_object=x))
                else:
                    self._log_data.append(self._RequestEntry(name=x.name, datatype=dt, request_object=x))
        elif isinstance(self.config.log_data, dict):
            self._log_data = [self._RequestEntry(name=name, datatype=dt, request_object=dt) for name, dt in self.config.log_data.items()]
        else:
            raise DataLoggerConfigError("`config.log_data` must be a list or a dict!")
        
        self._reduce()

        self._info = self.get_info()
        self._channels_used_count = len(self._effectively_log_data)
        self._total_number_of_samples = self.config.samples_per_channel*self._channels_used_count
        if self._channels_used_count > self._info.number_of_channels:
            raise DataLoggerConfigError("Exceeding number of channels!")
        if self._total_number_of_samples > self._info.sample_buffer_length:
            raise DataLoggerConfigError(f"`config.samples_per_channel` exceeds sample buffer length! You can use {math.floor(self._info.sample_buffer_length/self._channels_used_count)} at max.")
        self.rd.init()
        self.rd.set_sample_count(self.config.samples_per_channel*self._channels_used_count)
        self.rd.set_prescaler(self._down_sampling_factor-1)
        if self._trigger_type != Rd.TriggerType.UNCONDITIONAL:
            if self._trigger_on is None:
                raise DataLoggerConfigError("Trigger type specified but no trigger data given in `_trigger_on`!")
            channel_type, select = self._get_channel_type_and_select(datatype=self._trigger_on)
            self.rd.set_trigger_channel(channel_type=channel_type, select=select)
            if isinstance(self._trigger_on, DataLogger.DataTypeField):
                self.rd.set_shift_mask(shift=self._trigger_on.shift, mask=self._trigger_on.mask)
        
        # Set channels
        for datatype in self._effectively_log_data.values():
            channel_type, select = self._get_channel_type_and_select(datatype=datatype)
            self.rd.set_channel(
                channel_type=channel_type,
                select=select
            )

        self.rd.set_pretrigger_sample_count(self._pretrigger_samples)
        if self._trigger_type == Rd.TriggerType.UNCONDITIONAL:
            self.rd.enable_trigger(self._trigger_type, 0)
        else:
            if self._trigger_threshold is None:
                raise DataLoggerConfigError("Trigger type specified is conditional but no threshold given in `_trigger_threshold!")
            self.rd.enable_trigger(self._trigger_type, self._trigger_threshold)

    def is_pretriggering(self) -> bool:
        return self.rd.get_state() == Rd.State.PRETRIGGER

    def wait_for_pretrigger_completion(self) -> None:
        while self.is_pretriggering():
            pass

    def is_triggered(self) -> bool:
        return self.rd.get_state() >= Rd.State.CAPTURE
    
    def wait_for_trigger(self) -> None:
        while not self.is_triggered():
            pass

    def is_done(self) -> bool:
        return self.rd.get_state() == Rd.State.COMPLETE
    
    def wait_till_done(self) -> None:
        while not self.is_done():
            pass

    def download_log_step(self) -> bool:
        @dataclass
        class EffectiveDataSet:
            name: str
            datatype: DataLogger.DataType
            samples: list
        self._download_is_done = False
        self._downloaded_raw_data.append(self.rd.get_sample(self._download_offset))
        self._download_offset += 1
        if self._download_offset < self._total_number_of_samples:
            return True

        # Download is done - extract the data
        log_samples: List[EffectiveDataSet] = []
        for i in range(len(self._effectively_log_data)):
            name, datatype = list(self._effectively_log_data.items())[i]
            samples = self._downloaded_raw_data[i::self._channels_used_count]
            log_samples.append(EffectiveDataSet(name=name, datatype=datatype, samples=samples))

        period_s = self._down_sampling_factor/self._info.base_frequency_hz
        time_offset = self._pretrigger_samples*period_s
        time_vector = [i*period_s-time_offset for i in range(self.config.samples_per_channel)]
        self.log.rate_hz = self._info.base_frequency_hz/self._down_sampling_factor
        self.log.period_s = period_s
        self.log.time_vector = time_vector
        self.log.data = {}
        for entry in self._log_data:
            if entry.datatype.reuse_obj is None:
                use_datatype_obj = next((x for x in log_samples if x.datatype == entry.datatype))
            else:
                use_datatype_obj = next((x for x in log_samples if x.datatype == entry.datatype.reuse_obj))

            if isinstance(entry.datatype, DataLogger.DataTypeField):
                samples = [entry.datatype.get(sample) for sample in use_datatype_obj.samples]
            else:
                if entry.datatype.signed:
                    samples = [to_signed_32(sample) for sample in use_datatype_obj.samples]
                else:
                    samples = use_datatype_obj.samples

            self.log.data[entry.name] = DataLogger.LogData(
                samples=samples,
                request_object=entry.request_object,
            )

        self._downloaded_raw_data = []
        self._download_offset = 0
        self._download_is_done = True
        return False
    
    def download_log(self) -> None:
        while self.download_log_step():
            pass

    def _get_channel_type_and_select(self, datatype):
        if isinstance(datatype, DataLogger.DataTypeAp):
            select = ((datatype.axis << 24) & 0xFF00_0000) | ((datatype.index << 0) & 0x00FF_FFFF)
            return self.rd.Channel.AXIS_PARAMETER, select
        elif isinstance(datatype, DataLogger.DataTypeGp):
            select = ((datatype.bank << 24) & 0xFF00_0000) | ((datatype.index << 0) & 0x00FF_FFFF)
            return self.rd.Channel.GLOBAL_PARAMETER, select
        elif isinstance(datatype, DataLogger.DataTypeRegister) or isinstance(datatype, DataLogger.DataTypeField):
            select = ((datatype.block << 24) & 0xFF00_0000) | (datatype.address & 0x00FF_FFFF)
            return self.rd.Channel.REGISTER, select
        else:
            raise ValueError("Unknown DataType")
        
    def _transform_to_datatype(self, x: Union[Parameter, Register, Field]) -> DataLogger.DataType:
        if isinstance(x, Parameter):
            if x.category == ParameterGroup.Category.AXIS:
                return self.DataTypeAp.from_parameter(x)
            elif x.category == ParameterGroup.Category.GLOBAL:
                return self.DataTypeGp.from_parameter(x)
            else:
                raise DataLoggerConfigError("Parameter object must be of category AXIS or GLOBAL!")
        elif isinstance(x, Register):
            return self.DataTypeRegister.from_register(x)
        elif isinstance(x, Field):
            return self.DataTypeField.from_field(x)
        else:
            raise DataLoggerConfigError("Only Parameter, Register or Field objects can be transformed!")
        
    def _reduce(self):
        self._effectively_log_data = {}
        for entry in self._log_data:
            if isinstance(entry.datatype, DataLogger.DataTypeRegister) or isinstance(entry.datatype, DataLogger.DataTypeAp) or isinstance(entry.datatype, DataLogger.DataTypeGp):
                for existing_datatype in self._effectively_log_data.values():
                    if entry.datatype == existing_datatype:
                        entry.datatype.reuse_obj = existing_datatype
                        break
                else:
                    self._effectively_log_data[entry.name] = entry.datatype
            elif isinstance(entry.datatype, DataLogger.DataTypeField):
                for existing_datatype in self._effectively_log_data.values():
                    if isinstance(existing_datatype, (DataLogger.DataTypeField, DataLogger.DataTypeRegister)):
                        if all([
                            entry.datatype.block == existing_datatype.block,
                            entry.datatype.channel == existing_datatype.channel,
                            entry.datatype.address == existing_datatype.address,
                        ]):
                            entry.datatype.reuse_obj = existing_datatype
                            break
                else:
                    self._effectively_log_data[entry.name] = entry.datatype
            else:
                self._effectively_log_data[entry.name] = entry.datatype

    def _get_base_frequency_hz(self) -> int:
        return self.get_info().base_frequency_hz

    @property
    def download_progress(self) -> float:
        if self._download_is_done:
            return 100.0
        else:
            return 100*self._download_offset/self._total_number_of_samples
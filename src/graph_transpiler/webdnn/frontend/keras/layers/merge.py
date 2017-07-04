import keras

from webdnn.frontend.keras import KerasConverter
from webdnn.graph.operators.elementwise_mul import ElementwiseMul
from webdnn.graph.operators.elementwise_sum import ElementwiseSum
from webdnn.graph.operators.scalar_affine import ScalarAffine


@KerasConverter.register_handler("Add")
def _convert_add(converter: KerasConverter, k_op: keras.layers.Add):
    xs = [converter.get_variable(tensor) for tensor in converter.get_input_tensor(k_op)]

    y, = ElementwiseSum(None)(*xs)
    converter.set_variable(converter.get_output_tensor(k_op)[0], y)


@KerasConverter.register_handler("Multiply")
def _convert_multiply(converter: KerasConverter, k_op: keras.layers.Multiply):
    xs = [converter.get_variable(tensor) for tensor in converter.get_input_tensor(k_op)]

    y, = ElementwiseMul(None)(*xs)
    converter.set_variable(converter.get_output_tensor(k_op)[0], y)


# noinspection PyUnusedLocal
@KerasConverter.register_handler("Average")
def _convert_average(converter: KerasConverter, k_op: keras.layers.Average):
    xs = [converter.get_variable(tensor) for tensor in converter.get_input_tensor(k_op)]

    # FIXME: More effective implementation
    y, = ElementwiseSum(None)(*xs)
    y, = ScalarAffine(None, scale=1.0 / len(xs), bias=0)(y)
    converter.set_variable(converter.get_output_tensor(k_op)[0], y)


# noinspection PyUnusedLocal
@KerasConverter.register_handler("Maximum")
def _convert_maximum(converter: KerasConverter, k_op: keras.layers.Maximum):
    # TODO
    raise NotImplementedError('[KerasConverter] keras.layers.Maximum is not supported')


# noinspection PyUnusedLocal
@KerasConverter.register_handler("Dot")
def _convert_dot(converter: KerasConverter, k_op: keras.layers.Dot):
    # TODO
    raise NotImplementedError('[KerasConverter] keras.layers.Dot is not supported')

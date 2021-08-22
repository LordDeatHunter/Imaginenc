import string

from src import imaginenc

test_bytes = string.printable.encode()

test_image_colors = ['#000036', '#027079', '#746573', '#740000', '#000000',
                     '#000000', '#000000', '#000000', '#000000', '#000000',
                     '#000000', '#000000', '#000000', '#000000', '#000000',
                     '#000000', '#000000', '#000000', '#303132', '#333435',
                     '#363738', '#396162', '#636465', '#666768', '#696a6b',
                     '#6c6d6e', '#6f7071', '#727374', '#757677', '#78797a',
                     '#414243', '#444546', '#474849', '#4a4b4c', '#4d4e4f',
                     '#505152', '#535455', '#565758', '#595a21', '#222324',
                     '#252627', '#28292a', '#2b2c2d', '#2e2f3a', '#3b3c3d',
                     '#3e3f40', '#5b5c5d', '#5e5f60', '#7b7c7d', '#7e2009',
                     '#0a0d0b', '#0c0000']


def test_encode_bytes_to_colors():
    output = imaginenc.encode_bytes_to_colors(test_bytes, sign='pytest')
    assert output == test_image_colors


def test_decode_image_to_bytes():
    image = imaginenc.colors_to_image(test_image_colors)
    output = imaginenc.decode_image_to_bytes(image)
    assert output == test_bytes

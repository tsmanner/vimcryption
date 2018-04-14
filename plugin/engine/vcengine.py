"""
"""

from functools import reduce

__all__ = [
    "EncryptionEngine",
    "PassThrough",
    "BlockCipherEngine",
]


class EncryptionEngine:
    """
    Base vimcryption encryption engine.
    """

    def __init__(self):
        pass

    def encrypt(self, data, fh):
        # type: (Union[List[str], str], io.BytesIO):
        raise NotImplementedError("IOBase.encrypt must be implemented by a derived class!")

    def decrypt(self, fh, data):
        # type: (io.BytesIO, Union[List[str], str]):
        raise NotImplementedError("IOBase.decrypt must be implemented by a derived class!")


class PassThrough(EncryptionEngine):
    """
    Simple pass-through engine.
    """
    def encrypt(self, data, fh):
        # type: (Union[List[str], str], io.BytesIO):
        if isinstance(data, str):
            fh.write((data + "\n").encode("utf8"))
        else:
            for item in data:
                fh.write((item + "\n").encode("utf8"))

    def decrypt(self, fh, data):
        # type: (io.BytesIO, Union[List[str], str]):
        for bline in fh:
            line = bline.decode().rstrip("\n")
            if line != "":
                data.append(line)


class BlockCipherEngine(EncryptionEngine):
    """
    Base class for block ciphers.  Provides generic API for common utilities.
        Derived classes MUST define `self.encrypt_blocksize` and `self.decrypt_blocksize`
        in order to use the default encrypt/decrypt functions.  Derived classes
        may implement `encrypt` and `decrypt` instead.
    Supplied methods:
        Buffer iterator generator function
        BytesIO iterator generator function
        Block iterator generator function
        `encrypt` based on Block iterator
        `decrypt` based on block iterator
    """
    @staticmethod
    def buffer_iter(data):
        #type: List[str]
        for i, line in enumerate(data):
            for c in line:
                yield c
            if i < len(data):
                yield "\n"

    @staticmethod
    def byte_iter(fh):
        # type: io.ByteIO
        c = fh.read(1)
        while c != b"":
            yield c
            c = fh.read(1)

    @staticmethod
    def block_cipher(generator, block_size, pad):
        # type: (Iterable, int)
        block = []
        for item in generator:
            block.append(item)
            if len(block) == block_size:
                yield reduce(lambda a, b: a + b, block)
                block = []
        if len(block) > 0:
            while len(block) < block_size:
                block.append(pad)
            yield reduce(lambda a, b: a + b, block)

    def encrypt(self, data, fh):
        # type: (Union[Iterable[str], str], io.BytesIO)
        if isinstance(data, str):
            iterable = data
        else:
            iterable = self.buffer_iter(data)
        for block in self.block_cipher(iterable, self.encrypt_blocksize, ""):
            fh.write(self.encrypt_block(block))

    def decrypt(self, fh, data):
        # type: (io.BytesIO, Union[Iterable[str], str])
        line = ""
        for block in self.block_cipher(self.byte_iter(fh), self.decrypt_blocksize, b""):
            plaintext = self.decrypt_block(block)
            for c in plaintext:
                if c == "\n":
                    data.append(line)
                    line = ""
                else:
                    line += c
        if line != "":
            data.append(line)

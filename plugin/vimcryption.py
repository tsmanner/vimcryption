
import vim


class VCFileHandler():
    def __init__(self, config=None):
        if config:
            self.config = config

    def BufRead(self):
        """
        BufReadCmd: Before starting to edit a new buffer.  
        Should read the file into the buffer. 
        """
        file_name = vim.current.buffer.name
        with open(file_name, 'r+') as current_file:
            vim.current.buffer.append(current_file.readlines())

        # Vim adds an extra line at the top of the buffer 
        # We need to remove it or files keep getting longer
        del vim.current.buffer[0]

    def FileRead(self):
        """
        FileReadCmd: Before reading a file with a ":read" command.
        Should do the reading of the file.
        """
        file_name = vim.current.buffer.name
        with open(file_name, 'r+') as current_file:
            vim.current.buffer.append(current_file.readlines())

        # Vim adds an extra line at the top of the buffer 
        # We need to remove it or files keep getting longer
        del vim.current.buffer[0]

    def BufWrite(self):
        """
        BufWriteCmd: Before writing the whole buffer to a file.
        Should do the writing of the file and reset 'modified' if successful, unless '+' is in
        'cpo' and writing to another file |cpo-+|. The buffer contents should not be changed.
        """
        file_name = vim.current.buffer.name
        with open(file_name, 'w+') as current_file:
            current_file.writelines("\n".join(vim.current.buffer))

        vim.command(':set nomodified')

    def FileWrite(self):
        """
        FileWriteCmd: Before writing to a file, when not writing the
        whole buffer.  Should do the writing to the file.  Should not change the buffer.  Use the
        '[ and '] marks for the range of lines.
        """
        file_name = vim.current.buffer.name
        buf_start, buf_end = vim.buffer.mark("'["), vim.buffer.mark("']") 
        current_range = vim.buffer.range(buf_start, buf_end)

        with open(file_name, 'w+') as current_file:
            current_file.write("\n".join(current_range))

        vim.command(':set nomodified')

    def FileAppend(self):
        """
        FileAppendCmd: Before appending to a file.  Should do the
        appending to the file.  Use the '[ and '] marks for the range of lines.
        """
        file_name = vim.current.buffer.name
        buf_start, buf_end = vim.buffer.mark("'["), vim.buffer.mark("']") 
        current_range = vim.buffer.range(buf_start, buf_end)

        with open(file_name, 'a') as current_file:
            current_file.write("\n".join(current_range))

        vim.command(':set nomodified')



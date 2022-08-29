import os
import sys

class CustomerException(Exception):

    def __init__(self, error_message: Exception, error_details: sys) -> None:
        """
        This is a customized Exception class for generating 
        custom exception message.

        Parameters
        ----------
        error_message : Exception
            Exception instance created during occurrence of an error
        erro_details : sys
            sys instance capturing details about the current state

        Attributes
        ----------
        error_message : str
            Customized error message string.

        """
        
        super().__init__(error_message)
        self.error_message = CustomerException.get_custom_message(
                                                    error_message= error_message,
                                                    error_details= error_details
                                                )
        

    @staticmethod
    def get_custom_message(error_message: Exception, error_details: sys) -> str:
        """
        This function is responsible for generating a custom exception
        message based on the current exception that occurred.

        Parameters
        ----------
        error_message : Exception
            Exception instance created during occurrence of an error
        erro_details : sys
            sys instance capturing details about the current state

        Returns
        -------
        error_message : str
            Customized error message string.

        """

        _,_, exec_tb= error_details.exc_info()
        try_block_lineno= exec_tb.tb_lineno
        exception_block_lineno = exec_tb.tb_frame.f_lineno
        file_name= exec_tb.tb_frame.f_code.co_filename
        custom_error_message= f"""
        Error Occurred:
        File Name: [{file_name}]
        Line Num : [{try_block_lineno}]
        Exception Block: [{exception_block_lineno}]
        Error Message  : {error_message}
        """
        return custom_error_message

    
    def __str__(self) -> str:
        return self.error_message

    def __repr__(self) -> str:
        return CustomerException.__name__.str()

#!/usr/bin/env python3
""" Obfuscated personal data, done by filter_datum"""
import re


def filter_datum(fields: str, redaction: str, message: str,
                 separator: str) -> str:
    """ Obfuscated personal data is obtained from this function"""
    combo = "(?<=" + f"=)[^{separator}]*|(?<=" \
            .join(fields) + f"=)[^{separator}]*"
    return(re.sub(combo, '{}'.format(redaction), message))

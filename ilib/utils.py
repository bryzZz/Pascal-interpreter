def isNumber(char: str):
  return char.isdigit() or char == '.'


def isLetter(char: str):
  return ord(char) in range(97, 122)

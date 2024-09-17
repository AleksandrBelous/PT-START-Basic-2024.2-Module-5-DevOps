import re

"""
        Требования к паролю:
        - Пароль должен содержать не менее восьми символов.
        - Пароль должен включать как минимум одну заглавную букву (A–Z).
        - Пароль должен включать хотя бы одну строчную букву (a–z).
        - Пароль должен включать хотя бы одну цифру (0–9).
        - Пароль должен включать хотя бы один специальный символ, такой как !@#$%^&*().
"""

text = (
        'G4dL8pM*\n'
        'g4dl8pm*\n'
        'J#eK8dP4\n'
        'J1eK8dP4\n'
        'P4sS$eJ8\n'
        'PfsS$eJe\n'
        'M8pL4dK*\n'
        'M8PL4DK*\n'
        'E4dJ#8pS\n'
        'L8pK4dM*\n'
        'K4dP8eJ#\n'
        'J8pS4dL*\n'
        'P8eK4dM*\n'
        'M4dL8pJ#\n'
        'E8pS4dK*\n'
)
passwdRegex = re.compile(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}')  # формат

passwdList = passwdRegex.findall(text)
print(*passwdList, sep='\n')

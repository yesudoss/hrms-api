from jose import jwt
token2 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkB0ZXN0LmNvbSIsImV4cCI6MTcyOTkzMzg3NX0.BnicKvrm43uVsq0s7_NSj53rSbEXXSII2Dh0LKfHB_E'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkB0ZXN0LmNvbSIsImV4cCI6MTcyOTkzODUyOX0.hdLnao3BwmRW1Pe3Vhq2f4O6Mkqvjt-iP2XZ_xV39nk'
decoded_payload = jwt.decode(token, "supersecretkey123", algorithms=["HS256"])
print(decoded_payload)
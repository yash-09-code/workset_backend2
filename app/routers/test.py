# import sys
# from pathlib import Path

# # Add the project root directory to the Python path
# sys.path.append(str(Path(__file__).resolve().parents[2]))

# # Use an absolute import instead of relative
# from app.supabase import get_public_supabase

# db = get_public_supabase()
# result = db.auth.sign_in_with_password({ 
#     "email": "yash009@gmail.com", 
#     "password": "251198251198", 
# })
# print(result)

s = "IVX"

a = 0
for i in s:
    b = s.index(i)
    if i == "I":
        a += 1
    elif i == "V":
        if b == 0:
            a += 3
        else:
            a += 5
    elif i == "X":
        if b == 0:
            a += 8
        else:
            a += 10

print(a)

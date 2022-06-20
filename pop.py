# 데이터 처리 시 비밀번호만 별도로 해싱하는 방법

data = {
    "username" : "admin",
    "Password" : "p@ssw0rd",
    "fullname" : "Admin Eom",
    "email" : "admin@email.com",
    "gender" : "male",
    "age" : "30"
}

password = data.pop("password")

user = UserModel(**data)
user.set_password(password)
user.save()
from django.core.exceptions import ValidationError

def validate_str(value):
    str_list = ['!','@','#','$']
    val_count = 0
    for each in str_list:
        if each in value:
            val_count += 1
    if val_count < 1:
        raise ValidationError("密码必须包含'!','@','#','$'中至少一个")
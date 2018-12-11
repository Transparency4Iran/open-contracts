def persian_num_to_english(string):
    return string.strip().replace('۰', '0').replace('۱', '1').replace('۲', '2').replace('۳', '3') \
        .replace('۴', '4').replace('۵', '5').replace('۶', '6').replace('۷', '7'). \
        replace('۸', '8').replace('۹', '9')


def standard_persian(string):
    return string.strip().replace('ي', 'ی').replace('ؠ', 'ی').replace('ى', 'ی').replace('ك', 'ک') \
        .replace('ٶ', 'و').replace('ؤ', 'و').replace('‌', ' ')
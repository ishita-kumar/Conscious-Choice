import re
# txt="\u20ac0.25"
txt="$"
print(txt)
def validcurr(txt): 
    if txt[0]=="$":
        x= re.search("(?=.*?\d)^\$?(([1-9]\d{0,2}(,\d{3})*)|\d+)?(\.\d{2})?$", txt)
        if x:
            print("YES! We have a match!")
        else:
            print("ayyo")
    else:
        y= re.search("(?=.*?\d)^\\u20ac?(([1-9]\d{0,2}(,\d{3})*)|\d+)?(\.\d{2})?$", txt)
        if y:
            print("YES! We djdnkjhave a match!")
        else:
            print("ayyo") 


   


print(validcurr(txt))
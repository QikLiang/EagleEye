import os

count = 0
for fi in os.listdir('rename'):
    os.rename("rename\\" + fi, "dataset\\" + "Matt.1." + str(count) + ".jpg")
    count += 1

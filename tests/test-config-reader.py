from jarjar import jarjar
jj = jarjar(config='../.jarjar', message='hello2')
print(jj.default_channel)
print(jj.default_message)
print(jj.default_webhook)

# jj.text()

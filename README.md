# Эта программа представляет из себя простой чат-сервер для локальной сети
#
# Общие положения: все команды, полылаемые серверу имеют вид: <команда>параметры. Причем параметры
# могут и отсутствовать. После получения команды сервер посылает клиенту один символ: 0 в случае
# неудачного выполнения команды и 1 в случае успеха, также могут посылаться дополнительные данные
# после символа статуса команды.
#
# Поддерживаются следующие команды:
# 1. <login> - обязательная команда для каждого пользователя, которая говорит о том, что он зашел в чат.
# до нее пользователь не может делать никаких действий (получать и посылать сообщения и т.п.)
# после данной команды пользователю присваевается имя такое же как его IP адрес, например 1.2.3.4
#
# 2. <alias>NewName - команда, которая позволяет сменить ник пользователя на NewName. Данная команда
# изменит ник только в том случае, если в чате еще не существует пользователь с таким ником
#
# 3. <message>Текст - посылает сообщение "Текст"
#
# 4. <get messages>from - команда получения всех сообщений начиная с номера from. При этом клиенту сначала
# посылается число - количество сообщений, а потом все сообщения друг за другом
#
# 5. <server terminate> - команда завершающая работу сервера. Данная команда доступна только пользователю с
# ником admin
#
# 6. <logout> - команда, которая говорит, что пользователь вышел из чата
#
#Планируется изменить:

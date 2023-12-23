from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler,Filters
from telegram.ext import InlineQueryHandler
import json

# Replace 'YOUR_TOKEN' with the token you received from BotFather
TOKEN = 'THE TOKEN'

def retriveDatabase():
    f = open('database.txt','r')
    data = f.read()
    f.close()
    return json.loads(data)

database = retriveDatabase()

def storeDatabase():

    f = open('database.txt','w')
    f.write(json.dumps(database))
    f.close()


def databaseHandler(key,value=None,name=None,write=False):
    
    if(not key):
        
        return
    
    elif(write and not value):
        
        return
    
    else:
        
        if(write):
            
            database[key] = value
            database[key + "name"] = name
            storeDatabase()
            
        else:
            
            return database.get(key , "Not Available")
            
            
            
            

def start(update, context):
    update.message.reply_text('Welcome '+ update.message.from_user.first_name + ' to CP&DSA Club,\nuse /help to know how to use bot.')
    
def help(update, context):
    
    # update.message.reply_text("""Use /answers to get list of answers.
    #                         Type question serial number to buy the answer.
    #                         Answers will be available for free in last 15 mins.
    #                           """)

    update.message.reply_text("""Use /answers to get list of answers.
                            Type question serial number to get the answer.
                              """)
    

def total(update,context):
    
    database['total'] = int(context.args[0])
    update.message.reply_text("Total questions changed to : ", int(context.args[0]))
    
def welcome_message(update, context) -> None:
    for new_member in update.message.new_chat_members:
        update.message.reply_text(f"Welcome, {new_member.mention_html()}!\nUse /help to know more.")
    

def message_handler(update,context):
    
    user_message = update.message.text
    user_info = update.message
    # print(user_info)

    if(user_info.from_user.id == 1299071374):
        messageLineArray = user_message.splitlines()
        metaData = messageLineArray[0].split()
        
        try:
            int(metaData[0])
            databaseHandler(metaData[0],user_message,messageLineArray[0],True)
            update.message.reply_text("Answer Added To Database,\nHere's a look")
            update.message.reply_text(databaseHandler(metaData[0],write=False))
            return

        except:
            pass
            
    
    try:
        int(user_message)
        update.message.reply_text(databaseHandler(user_message,write=False))
    except:
        pass
        

def answers(update, context):
    
    listAnswers = ""
    
    for j in range(1,int(database.get('total',1))+1):
        
        listAnswers += str(j) + ". " + database.get(str(j)+"name" , "Not available") +'\n'
        
    update.message.reply_text(listAnswers)
    
def refreshForContest(update, context):
    
    if(update.message.from_user.id == 1299071374):
        global database
        database = {}
        storeDatabase()
        update.message.reply_text("We're all set for new contest.")
        
    else:
        
        update.message.reply_text("Only Admin Access.")
        

def main():
    updater = Updater(TOKEN,use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("total", total))
    dp.add_handler(CommandHandler("answers", answers))
    dp.add_handler(CommandHandler("refresh", refreshForContest))
    dp.add_handler(MessageHandler(filters=Filters.all,callback=message_handler))
    # dp.add_handler(CommandHandler("ban", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

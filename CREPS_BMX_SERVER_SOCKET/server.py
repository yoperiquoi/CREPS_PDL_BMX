# External Imports
import eventlet
import socketio
import pandas as pd
import requests
import copy

# Internal Imports
from utils import init_record_df



"""
    Global var
        @GLOBAL df : current race records
        @GLOBAL list_users : list of the users connected
        @GLOBAL db_race_id : current race ID
"""
df = init_record_df()
list_users = dict()
db_race_id = -1 



"""
    Socket.io Server socket
        On a WSGI app server
"""
sio = socketio.Server(cors_allowed_origins=[], cors_credentials=False)
app = socketio.WSGIApp(sio)



@sio.event
def connect(sid, environ, auth) :
    """
        @function : connect
        @param : sid - client ID who emitted the event
        @param : environ - client environnement (headers)
        @param : auth - Client auth
    """

    print('New Sensor connected :', sid, auth)

    sio.emit('client_connected', {
        "username" : auth['Username'],
        "id" : auth['id'], 
        "sid" : sid
    })

    global list_users
    list_users[sid] = {
        'username' : auth['Username'],
        'id' : auth['id'],
        'sid' : sid
    }

    return 1, "Success" 
# def connect(sid, environ, auth)



@sio.event
def disconnect(sid) :
    """
        @disconnect
        @param : sid - client who emitted the event id
    """

    print('disconnect ', sid)

    sio.emit('client_disconnected', {
        "sid" : sid
    })

    global list_users
    del list_users[sid]

    return 1, "Success"
# def disconnect(sid)



@sio.on('sensor_record')
def record(sid, data) :
    """
        @function : record
        @param : sid - client who emitted the event id
        @param : data - data passed to the 'sensor_record' event
    """

    print('____________________________________________')
    print('Inserted Data : ', data)

    global df
    df = df.append(data, ignore_index=True)

    return 1, "Success"
#def another_event(sid, data):



@sio.on('race_start')
def start_race_event(sid, data) :
    """
        @function : start_race_event
        @param : sid - client who emitted the event id
        @param : data - data passed to the 'race_start' event
    """

    print('______________________________________________')
    print(data)
    print('______________________________________________')

    global df
    df = init_record_df()

    global db_race_id
    db_race_id = data['K_ID']
    k_piste = data['K_PISTE']

    piste_info = requests.get(f'http://51.75.124.195:5000/getPiste?K_ID={k_piste}')
    
    piste_info = piste_info.json()['res'][0]

    result = {
        'borne_1' : {
            'lat' : piste_info['F_ARRIVEE1_LATITUDE'],
            'lon' : piste_info['F_ARRIVEE1_LONGITUDE']
        },

        'borne_2' : {
            'lat' : piste_info['F_ARRIVEE2_LATITUDE'],
            'lon' : piste_info['F_ARRIVEE2_LONGITUDE']
        }
    }

    print('____________________________________________________________________')
    print(result)
    print('____________________________________________________________________')

    print('A new race started : ', db_race_id)

    sio.emit('start_record', result)

    return 1, "Success"
# def start_race_event(sid, data)



@sio.on('race_end')
def end_race_event(sid, data) :
    """
        @function : end_race_event
        @param : sid - client id who emitted the event
        @param : data - data passed to the event 'race_end'
    """

    global df

    global db_race_id
    df['K_COURSE'] = db_race_id

    print('_________________________________________________')
    print("len df to insert in db : ", )
    df = df.where(pd.notnull(df), -999999999)
    df.to_csv('./race_record.csv', index=None)

    files = {'file': open('./race_record.csv','r')}
    r = requests.post('http://51.75.124.195:5000/file-upload', files=files)

    df = init_record_df()

    sio.emit('end_record', {}) 
    sio.sleep(1)

    global list_users
    c_id_list = copy.copy(list(list_users.keys()))
    for c_id in c_id_list :
        sio.disconnect(c_id)
 
    db_race_id = -1


    return 1, "Success"
# def end_race_event(sid, data)



@sio.on('get_connected')
def get_list_connected(sid, data) :
    """
        @function : get_list_connected
        @param : sid - client ID who emitted the event
        @param : data - data passed to the event 'race_end'
    """

    global list_users
    sio.emit('s_connect', list_users)

    return 1, "Success"
# def get_list_connected()



@sio.on('finish_detected')
def send_arrived(sid, data):
    """
        @function : send_arrived
        @param : sid - Client ID who emitted the event
        @param : data - data passed to the event 'finished_detected'
    """    

    sio.disconnect(sid)

    return 1, "Success"
# def send_arrived(sid, data)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 37591)), app)


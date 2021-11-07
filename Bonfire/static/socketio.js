document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    let room;

    //displays incoming messsages
    socket.on('message', data => {
    
        const p = document.createElement('p');
        const br = document.createElement('br');
        const b_username = document.createElement('b');
        const small_timestamp = document.createElement('small');

        if( data.username){

            b_username.innerHTML = data.username;
            small_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = b_username.outerHTML + ": " + data.msg + "     " + small_timestamp.outerHTML + br.outerHTML;
            document.querySelector('#display-message-section').append(p);
        }
        else{
            printSysMsg(data.msg)
        }

    });

    
    //send message
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value,
                    'username': username,
                    'room' : room
                });
        //Make text box empty after clicking send
        document.querySelector('#user_message').value = "";
    };

    //selecting a room from options
    document.querySelectorAll('#room_select').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if(newRoom == room){
                msg = `You are already in ${room} community`;
                printSysMsg(msg);
                
            }
            else{
                document.querySelector('#grpName').innerHTML = "";
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
                grpname = `${room}`;
                showGrpName(grpname);
            }
        }
    });

    // Make 'enter' key submit message
    let msg = document.getElementById("#user_message");
    msg.addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.key === 'Enter') {
            document.getElementById("#send_message").click();
        }
    });

    function leaveRoom(room){
        socket.emit('leave', {'username': username, 'room': room});
    }

    function joinRoom(room){
        socket.emit('join', {'username': username, 'room': room});
        //clear old text after joining new room
        document.querySelector('#display-message-section').innerHTML = "";
    }
    // print message to text area
    function printSysMsg(msg){
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }

    function showGrpName(msg){

        document.querySelector('#grpName').append(msg);
    }

})
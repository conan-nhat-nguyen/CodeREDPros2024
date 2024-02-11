// collect DOMs
let mediaRecorder, chunks = [], audioURL = ''

// mediaRecorder setup for audio
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
    console.log('mediaDevices supported..')

    navigator.mediaDevices.getUserMedia({
        audio: true
    }).then(stream => {
        mediaRecorder = new MediaRecorder(stream)

        mediaRecorder.ondataavailable = (e) => {
            chunks.push(e.data)
        }

        mediaRecorder.onstop = async () => {
            const blob = new Blob(chunks, {'type': 'audio/wav; codecs=opus'})
            
            chunks = []
        
            let formData = new FormData()
            formData.append('audio', blob, 'audio.wav')

            fetch('/record', {
                method: 'POST',
                headers: {
                    'Content-Type': 'audio/wav'
                },
                body: formData
            }).then(response => {
                return response.json()
            }).then(data => {
                console.log(data)
            }).catch(error => {
                console.log('Following error has occured : ',error)
            })

        }
    }).catch(error => {
        console.log('Following error has occured : ',error)
    })
}

const record = () => {
    mediaRecorder.start()
}

const stopRecording = () => {
    mediaRecorder.stop()
}


document.getElementById('mic').addEventListener('click', () => {

    const mic = document.getElementById('mic');
    const status = mic.getAttribute('status');
    if (status === 'off') {
        mic.setAttribute('status', 'on');
        mic.classList.add('fa-microphone-slash');
        mic.classList.remove('fa-microphone');
        record();
    } else {
        mic.setAttribute('status', 'off');
        mic.classList.add('fa-microphone');
        mic.classList.remove('fa-microphone-slash');
        stopRecording();
    }
});
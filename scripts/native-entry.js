// Este archivo lo empaqueta GitHub; edita www/index.html para cambiar la interfaz.
import { Capacitor, SystemBars } from '@capacitor/core';
import { SpeechRecognition } from '@capgo/capacitor-speech-recognition';
import { TextToSpeech } from '@capacitor-community/text-to-speech';
if(Capacitor.isNativePlatform()) {
  window.SIMO_NATIVE = {
    async listen() {
      const avail=await SpeechRecognition.available({language:'es-ES'});
      if(avail && avail.available === false) throw new Error('Tu Android no tiene un servicio de reconocimiento de voz disponible. Puedes escribir en el chat.');
      const perm=await SpeechRecognition.requestPermissions();
      if(perm && perm.speechRecognition==='denied') throw new Error('El micrófono está bloqueado. Activa el permiso de voz en Ajustes de Android.');
      const result=await SpeechRecognition.start({language:'es-ES',maxResults:1,popup:true,partialResults:false});
      return (result?.matches||[])[0]||'';
    },
    async speak(text,rate=1){
      await TextToSpeech.stop().catch(()=>{});
      return TextToSpeech.speak({text:String(text).slice(0,1000),lang:'es-ES',rate,pitch:1,volume:1,queueStrategy:1});
    },
    async setImmersive(enabled){if(enabled)await SystemBars.hide(); else await SystemBars.show()}
  };
}

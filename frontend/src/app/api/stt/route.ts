import { NextResponse } from 'next/server';

const SARVAM_API_KEY = process.env.SARVAM_API_KEY || '';
const SARVAM_STT_URL = 'https://api.sarvam.ai/speech-to-text';

export async function POST(req: Request) {
  try {
    if (!SARVAM_API_KEY) {
      return NextResponse.json(
        { success: false, error: 'SARVAM_API_KEY not configured on the server' },
        { status: 500 }
      );
    }

    const formData = await req.formData();
    const audioFile = formData.get('file') as File | null;
    const languageCode = (formData.get('language') as string) || 'hi-IN';

    if (!audioFile) {
      return NextResponse.json(
        { success: false, error: 'audio file is required' },
        { status: 400 }
      );
    }

    // Browser MediaRecorder sends "audio/webm;codecs=opus"
    // Sarvam rejects the codec suffix — strip to clean base MIME type
    const rawMime = audioFile.type || 'audio/webm';
    const cleanMime = rawMime.split(';')[0]; // "audio/webm"

    // Rebuild the Blob with the clean MIME type
    const audioBuffer = await audioFile.arrayBuffer();
    const cleanBlob = new Blob([audioBuffer], { type: cleanMime });

    // Give it a filename with the right extension
    const ext = cleanMime.includes('mp3')
      ? 'mp3'
      : cleanMime.includes('wav')
      ? 'wav'
      : cleanMime.includes('ogg')
      ? 'ogg'
      : 'webm';
    const fileName = `recording.${ext}`;

    // Forward to Sarvam as multipart/form-data
    const sarvamForm = new FormData();
    sarvamForm.append('file', cleanBlob, fileName);
    sarvamForm.append('language_code', languageCode);
    sarvamForm.append('model', 'saaras:v3');

    const resp = await fetch(SARVAM_STT_URL, {
      method: 'POST',
      headers: {
        'api-subscription-key': SARVAM_API_KEY,
      },
      body: sarvamForm,
    });

    if (!resp.ok) {
      const errBody = await resp.text();
      console.error('Sarvam STT API error:', resp.status, errBody);
      return NextResponse.json(
        { success: false, error: `Sarvam STT error (${resp.status}): ${errBody}` },
        { status: 502 }
      );
    }

    const data = await resp.json();
    // Sarvam returns { request_id, transcript, language_code, language_probability }
    return NextResponse.json({
      success: true,
      text: data.transcript || '',
      // Return detected language so the frontend can switch TTS/assistant language
      detectedLanguage: data.language_code || languageCode,
    });
  } catch (error) {
    console.error('STT route error:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to transcribe audio' },
      { status: 500 }
    );
  }
}

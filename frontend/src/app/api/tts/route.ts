import { NextResponse } from 'next/server';

const SARVAM_API_KEY = process.env.SARVAM_API_KEY || '';
const SARVAM_TTS_URL = 'https://api.sarvam.ai/text-to-speech';

// Valid speakers for bulbul:v3 strictly per Sarvam AI's API:
// aditya, ritu, ashutosh, priya, neha, rahul, pooja, rohan, simran, kavya,
// amit, dev, ishita, shreya, ratan, varun, manan, sumit, roopa, kabir,
// aayan, shubh, advait, anand, tanya, tarun, sunny, mani, gokul, vijay,
// shruti, suhani, mohit, kavitha, rehan, soham, rupali
const SPEAKER_MAP: Record<string, string> = {
  'mr-IN': 'rupali', // Native Marathi female speaker for bulbul:v3
  'hi-IN': 'pooja',  // Natural Hindi female speaker
  'en-IN': 'neha',   // Indian English female speaker
};

export async function POST(req: Request) {
  try {
    const { text, languageCode = 'mr-IN', speaker: requestedSpeaker } = await req.json();

    if (!text) {
      return NextResponse.json(
        { success: false, error: 'text is required' },
        { status: 400 }
      );
    }

    if (!SARVAM_API_KEY) {
      return NextResponse.json(
        { success: false, error: 'SARVAM_API_KEY not configured on the server' },
        { status: 500 }
      );
    }

    // bulbul:v3 max 1500 chars per request
    const textChunk = text.slice(0, 1500);
    const speaker = requestedSpeaker || SPEAKER_MAP[languageCode] || 'rupali';

    const payload = {
      text: textChunk,
      target_language_code: languageCode, // bulbul:v3 requires target_language_code
      speaker: speaker,
      model: 'bulbul:v3',                 // Updated from deprecated bulbul:v2
      speech_sample_rate: 22050,
      enable_preprocessing: true,
    };

    const resp = await fetch(SARVAM_TTS_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-subscription-key': SARVAM_API_KEY,
      },
      body: JSON.stringify(payload),
    });

    if (!resp.ok) {
      const errBody = await resp.text();
      console.error('Sarvam TTS API error:', resp.status, errBody);
      return NextResponse.json(
        { success: false, error: `Sarvam TTS error (${resp.status}): ${errBody}` },
        { status: 502 }
      );
    }

    const data = await resp.json();
    const audioBase64 = data.audios?.[0] ?? '';

    if (!audioBase64) {
      return NextResponse.json(
        { success: false, error: 'No audio returned from Sarvam TTS' },
        { status: 502 }
      );
    }

    return NextResponse.json({ success: true, audio: audioBase64 });
  } catch (error) {
    console.error('TTS route error:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to generate speech' },
      { status: 500 }
    );
  }
}

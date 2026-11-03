from typing import List, Dict, Any, Optional
from app.ai.base import BaseAIProvider

class LocalFallbackProvider(BaseAIProvider):
    def get_provider_name(self) -> str:
        return "local-deterministic-fallback"

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        language: str = "en"
    ) -> str:
        last_message = messages[-1]["content"] if messages else ""
        query_lower = last_message.lower()

        if "income" in query_lower or "उत्पन्न" in query_lower or "आय" in query_lower:
            if language == "mr":
                return (
                    "उत्पन्नाच्या दाखल्यासाठी (Income Certificate) अधिकृत वैधानिक शुल्क ₹३३.६० आहे. "
                    "आपले सरकार पोर्टलवर अर्ज केल्यानंतर हा दाखला १५ कामकाजाच्या दिवसांत मिळतो. "
                    "आवश्यक कागदपत्रांमध्ये ओळख पुरावा, पत्त्याचा पुरावा आणि उत्पन्नाचा पुरावा (तलाठी अहवाल/फॉर्म १६) आवश्यक आहे."
                )
            elif language == "hi":
                return (
                    "आय प्रमाण पत्र (Income Certificate) के लिए आधिकारिक वैधानिक शुल्क ₹33.60 है। "
                    "आपके सरकार पोर्टल पर आवेदन के बाद यह 15 कार्य दिवसों में जारी किया जाता है। "
                    "पहचान प्रमाण, पते का प्रमाण और आय प्रमाण (तलाठी रिपोर्ट/फॉर्म 16) अनिवार्य हैं।"
                )
            return (
                "For an Income Certificate in Maharashtra, the statutory fee is ₹33.60 on the Aaple Sarkar portal. "
                "The guaranteed delivery timeline under the Right to Services Act is 15 working days. "
                "Required documents include Identity Proof, Address Proof, and Income Proof (Talathi Report / Form 16)."
            )

        if "domicile" in query_lower or "रहिवासी" in query_lower or "निवास" in query_lower:
            if language == "mr":
                return (
                    "अधिवास प्रमाणपत्रासाठी (Domicile Certificate) अर्जदाराचे महाराष्ट्रात सलग किमान १५ वर्षे वास्तव्य असणे बंधनकारक आहे. "
                    "प्रक्रियेची मुदत १५ कामकाजाचे दिवस असून अधिकृत शुल्क ₹३३.६० आहे."
                )
            elif language == "hi":
                return (
                    "अधिवास प्रमाण पत्र (Domicile Certificate) के लिए महाराष्ट्र में कम से कम 15 वर्ष का निरंतर निवास अनिवार्य है। "
                    "इसकी प्रक्रिया में 15 कार्य दिवस लगते हैं और वैधानिक शुल्क ₹33.60 है।"
                )
            return (
                "For a Domicile Certificate, you must have resided continuously in Maharashtra for at least 15 years. "
                "Statutory processing time is 15 working days with a government fee of ₹33.60."
            )

        if "caste" in query_lower or "जात" in query_lower or "जाति" in query_lower:
            if language == "mr":
                return (
                    "जात प्रमाणपत्रासाठी (Caste Certificate) अर्जदाराकडे विहित वर्षापूर्वीचा महसुली/शालेय पुरावा असणे आवश्यक आहे. "
                    "कालावधी २१ कामकाजाचे दिवस आणि शुल्क ₹३३.६० आहे."
                )
            return (
                "For a Caste Certificate in Maharashtra, historical family residence and caste proof prior to the deemed cut-off date is required. "
                "Statutory processing time is 21 working days with a fee of ₹33.60."
            )

        # General helpful guidance
        if language == "mr":
            return (
                "मी सारथी (SAARTHI) सहाय्यक आहे. मी आपल्याला महाराष्ट्र शासनाच्या विविध सेवा, लागणारी कागदपत्रे आणि अधिकृत अर्ज प्रक्रियेबद्दल मदत करू शकतो. "
                "कृपया विशिष्ट सेवेचे नाव विचारा (उदा. उत्पन्नाचा दाखला, अधिवास प्रमाणपत्र, शिष्यवृत्ती)."
            )
        elif language == "hi":
            return (
                "मैं सारथी (SAARTHI) सहायक हूँ। मैं महाराष्ट्र शासन की विभिन्न सेवाओं, आवश्यक दस्तावेजों और आधिकारिक आवेदन प्रक्रिया में आपकी सहायता कर सकता हूँ। "
                "कृपया किसी विशिष्ट सेवा के बारे में पूछें (जैसे आय प्रमाण पत्र, अधिवास प्रमाण पत्र)।"
            )
        return (
            "I am the SAARTHI guidance assistant. I can help you understand Maharashtra government service requirements, mandatory documents, statutory fees, and official application portals. "
            "Please ask about a specific service like Income Certificate, Domicile Certificate, or Scholarships."
        )

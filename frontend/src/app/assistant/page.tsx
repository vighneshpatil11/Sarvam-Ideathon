"use client";

import { PageIntro, Disclaimer } from "@/components/UI";
import { AssistantWidget } from "@/components/AssistantWidget";
import { useApp } from "@/context/AppContext";

export default function AssistantPage() {
  const { language, t } = useApp();
  return (
    <div className="container page-container assistant-page">
      <PageIntro
        eyebrow={language === "mr" ? "नागरिक मार्गदर्शन केंद्र" : "CITIZEN GUIDANCE"}
        title={language === "mr" ? "आपले सरकार व्हॉइस असिस्टंट" : "Aaple Sarkar AI Voice Guide"}
        description={
          language === "mr"
            ? "महाराष्ट्रातील शासकीय सेवांची संपूर्ण माहिती, कागदपत्रांची यादी आणि पायरी-दर-पायरी मार्गदर्शन मिळवा. मराठी, हिंदी किंवा इंग्रजीत बोला."
            : t("assistantIntro")
        }
      />
      <AssistantWidget />
      <Disclaimer />
    </div>
  );
}

from typing import Dict, Any, List, Tuple
from app.models import Service, EligibilityRule, EligibilityQuestion
from app.schemas import RuleResultOut, EligibilityEvaluationResponse, SourceOut

def evaluate_service_eligibility(
    service: Service,
    answers: Dict[str, Any],
    language: str = "en"
) -> EligibilityEvaluationResponse:
    rules: List[EligibilityRule] = service.eligibility_rules
    questions: List[EligibilityQuestion] = service.eligibility_questions

    if not rules:
        return EligibilityEvaluationResponse(
            status="unable_to_determine",
            summary="Eligibility criteria not yet formalized for this service.",
            explanation="The formal statutory rule logic for this service is under review by authorities. Please consult the official portal directly.",
            missing_information=[],
            rule_results=[],
            sources=[
                SourceOut(
                    id=s.id,
                    title=s.title,
                    url=s.url,
                    publisher=s.publisher,
                    source_type=s.source_type,
                    supports=s.supports,
                    last_checked_at=s.last_checked_at.isoformat() if s.last_checked_at else None
                ) for s in service.sources
            ]
        )

    # Check for missing required questions
    missing_fields: List[str] = []
    for q in questions:
        if q.required and q.field_key not in answers:
            label = q.label_en
            if language == "hi" and q.label_hi:
                label = q.label_hi
            elif language == "mr" and q.label_mr:
                label = q.label_mr
            missing_fields.append(f"{label} ({q.field_key})")

    if missing_fields:
        return EligibilityEvaluationResponse(
            status="more_information_required",
            summary="Additional information is required to evaluate eligibility.",
            explanation=f"Please answer all mandatory questions: {', '.join(missing_fields)}.",
            missing_information=missing_fields,
            rule_results=[],
            sources=[
                SourceOut(
                    id=s.id,
                    title=s.title,
                    url=s.url,
                    publisher=s.publisher,
                    source_type=s.source_type,
                    supports=s.supports,
                    last_checked_at=s.last_checked_at.isoformat() if s.last_checked_at else None
                ) for s in service.sources
            ]
        )

    rule_results: List[RuleResultOut] = []
    disqualified = False
    disqualification_reasons: List[str] = []

    for rule in rules:
        user_val = answers.get(rule.field_key)
        passed = False

        if user_val is None:
            # Field missing for this rule
            passed = False
        else:
            try:
                op = rule.operator.lower()
                exp_str = rule.expected_value.strip()

                if op in ("eq", "=="):
                    if isinstance(user_val, bool):
                        passed = (user_val == (exp_str.lower() in ("true", "1", "yes")))
                    else:
                        passed = (str(user_val).strip().lower() == exp_str.lower())
                elif op in ("ne", "!="):
                    if isinstance(user_val, bool):
                        passed = (user_val != (exp_str.lower() in ("true", "1", "yes")))
                    else:
                        passed = (str(user_val).strip().lower() != exp_str.lower())
                elif op in ("lte", "<="):
                    passed = float(user_val) <= float(exp_str)
                elif op in ("lt", "<"):
                    passed = float(user_val) < float(exp_str)
                elif op in ("gte", ">="):
                    passed = float(user_val) >= float(exp_str)
                elif op in ("gt", ">"):
                    passed = float(user_val) > float(exp_str)
                elif op == "in":
                    allowed = [x.strip().lower() for x in exp_str.split(",")]
                    passed = str(user_val).strip().lower() in allowed
                else:
                    passed = False
            except (ValueError, TypeError):
                passed = False

        fail_msg = rule.failure_message_en
        if language == "hi" and rule.failure_message_hi:
            fail_msg = rule.failure_message_hi
        elif language == "mr" and rule.failure_message_mr:
            fail_msg = rule.failure_message_mr

        rule_results.append(
            RuleResultOut(
                rule_code=rule.rule_code,
                description=rule.description,
                passed=passed,
                failure_message=fail_msg if not passed else None
            )
        )

        if not passed and rule.is_disqualifying:
            disqualified = True
            disqualification_reasons.append(fail_msg)

    sources_out = [
        SourceOut(
            id=s.id,
            title=s.title,
            url=s.url,
            publisher=s.publisher,
            source_type=s.source_type,
            supports=s.supports,
            last_checked_at=s.last_checked_at.isoformat() if s.last_checked_at else None
        ) for s in service.sources
    ]

    if disqualified:
        summary_text = "Based on verified statutory guidelines, you appear potentially not eligible."
        if language == "hi":
            summary_text = "सत्यापित वैधानिक दिशानिर्देशों के अनुसार, आप संभावित रूप से पात्र नहीं दिखते हैं।"
        elif language == "mr":
            summary_text = "सत्यापित वैधानिक मार्गदर्शक तत्त्वांच्या आधारे, आपण संभाव्यतः अपात्र दिसत आहात."

        explanation_text = " ".join(disqualification_reasons) + " Note: This is an automated preliminary determination and does not replace official departmental review."
        return EligibilityEvaluationResponse(
            status="potentially_not_eligible",
            summary=summary_text,
            explanation=explanation_text,
            missing_information=[],
            rule_results=rule_results,
            sources=sources_out
        )

    summary_text = "Based on the information provided, you appear potentially eligible."
    if language == "hi":
        summary_text = "प्रदान की गई जानकारी के आधार पर, आप संभावित रूप से पात्र प्रतीत होते हैं।"
    elif language == "mr":
        summary_text = "दिलेल्या माहितीच्या आधारे, आपण संभाव्यतः पात्र दिसत आहात."

    explanation_text = "You meet the preliminary eligibility criteria established by official departmental rules. Final approval is subject to original document verification by the competent revenue authority."
    if language == "hi":
        explanation_text = "आप आधिकारिक विभागीय नियमों द्वारा स्थापित प्रारंभिक पात्रता मानदंडों को पूरा करते हैं। अंतिम अनुमोदन सक्षम राजस्व प्राधिकरण द्वारा मूल दस्तावेज सत्यापन के अधीन है।"
    elif language == "mr":
        explanation_text = "आपण अधिकृत विभागीय नियमांनुसार निश्चित केलेले प्राथमिक पात्रता निकष पूर्ण करता. अंतिम मंजुरी सक्षम महसूल प्राधिकरणाद्वारे मूळ कागदपत्रांच्या पडताळणीवर अवलंबून असते."

    return EligibilityEvaluationResponse(
        status="potentially_eligible",
        summary=summary_text,
        explanation=explanation_text,
        missing_information=[],
        rule_results=rule_results,
        sources=sources_out
    )

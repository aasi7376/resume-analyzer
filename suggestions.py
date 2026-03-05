def generate_suggestions(missing_keywords, final_score):
    suggestions = []

    # Score based suggestions
    if final_score >= 70:
        suggestions.append(
            "✅ Excellent match! Your resume is well aligned with this job description."
        )
    elif final_score >= 40:
        suggestions.append(
            "⚠️ Moderate match. Focus on adding the missing keywords to improve your score."
        )
    else:
        suggestions.append(
            "❌ Weak match. Your resume needs significant tailoring for this role."
        )

    # Missing keyword suggestions
    if missing_keywords:
        top_missing = missing_keywords[:8]
        suggestions.append(
            f"📌 Add these important missing keywords to your resume: "
            f"{', '.join(top_missing)}"
        )
        suggestions.append(
            "📝 Update your skills section to include technologies "
            "and tools mentioned in the job description."
        )
        suggestions.append(
            "🔍 Use the exact terminology from the job description "
            "wherever applicable in your resume."
        )
        suggestions.append(
            "📄 Rewrite your summary or objective section to reflect "
            "the key requirements of this role."
        )
    else:
        suggestions.append(
            "🌟 Your resume covers all key terms from the job description. "
            "Focus on quantifying your achievements."
        )

    # General suggestions
    suggestions.append(
        "📊 Quantify your achievements where possible "
        "(e.g. 'Improved performance by 30%')."
    )
    suggestions.append(
        "🎯 Keep your resume to 1-2 pages and ensure "
        "it is ATS friendly with clean formatting."
    )

    return suggestions
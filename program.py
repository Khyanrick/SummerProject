import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# ---------- Extract text from PDF ----------
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ---------- Rank Resumes with ML ----------
def rank_resumes(job_description, resume_texts, resume_names):
    # Combine texts
    documents = [job_description] + resume_texts
    labels = [1] + [0] * len(resume_texts)  # 1 = match (job desc), 0 = not match (resumes)

    # Vectorize with TF-IDF
    tfidf = TfidfVectorizer().fit_transform(documents).toarray()

    # Train Decision Tree Classifier
    clf = DecisionTreeClassifier()
    clf.fit(tfidf, labels)

    # Cosine similarity between job description and each resume
    job_vec = tfidf[0]
    resume_vecs = tfidf[1:]
    cosine_scores = cosine_similarity([job_vec], resume_vecs).flatten()

    # Predict if resume matches the job (not used directly here)
    predictions = clf.predict(resume_vecs)

    # Combine and sort by score
    ranked = sorted(zip(resume_names, cosine_scores, predictions), key=lambda x: x[1], reverse=True)
    return ranked

# ---------- Upload Resumes and Rank ----------
def upload_and_rank():
    resume_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if not resume_paths:
        return

    # Get job description
    job_description = job_description_box.get("1.0", tk.END).strip()
    if not job_description:
        messagebox.showerror("Error", "Please enter a job description.")
        return

    # Get threshold
    try:
        match_threshold = float(threshold_var.get()) / 100.0
    except ValueError:
        messagebox.showerror("Error", "Invalid match threshold value.")
        return

    resume_texts = []
    resume_names = []

    for path in resume_paths:
        text = extract_text_from_pdf(path)
        resume_texts.append(text)
        resume_names.append(os.path.basename(path))

    ranked = rank_resumes(job_description, resume_texts, resume_names)

    # Display results
    result_box.delete("1.0", tk.END)
    names = []
    scores = []

    for i, (name, score, _) in enumerate(ranked, 1):
        percent = round(score * 100, 2)
        label = "✅ Match" if score >= match_threshold else "❌ Not Match"
        result_box.insert(tk.END, f"{i}. {name} - Score: {percent}% - {label}\n")
        names.append(name)
        scores.append(percent)

    # Bar chart of scores
    plt.figure(figsize=(8, 4))
    plt.barh(names[::-1], scores[::-1], color='lightgreen')
    plt.xlabel("Match Percentage")
    plt.title("Resume Ranking (TF-IDF + ML)")
    plt.tight_layout()
    plt.show()

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("ML-Powered Resume Ranker")
root.geometry("620x650")

# Job Description Input
tk.Label(root, text="Job Description:", font=('Arial', 12, 'bold')).pack(pady=5)
job_description_box = scrolledtext.ScrolledText(root, height=5, width=70)
job_description_box.pack(pady=5)

# Match Threshold Input
threshold_frame = tk.Frame(root)
threshold_frame.pack(pady=5)
tk.Label(threshold_frame, text="Match Threshold (%):", font=('Arial', 10)).pack(side=tk.LEFT)
threshold_var = tk.DoubleVar(value=20.0)  # default threshold 20%
threshold_entry = tk.Entry(threshold_frame, textvariable=threshold_var, width=5)
threshold_entry.pack(side=tk.LEFT)

# Upload Button
upload_btn = tk.Button(root, text="📂 Upload Resumes and Rank", font=('Arial', 12), command=upload_and_rank)
upload_btn.pack(pady=10)

# Result Box
tk.Label(root, text="Ranking Results:", font=('Arial', 12, 'bold')).pack(pady=5)
result_box = scrolledtext.ScrolledText(root, height=12, width=70)
result_box.pack(pady=5)

# Run GUI
root.mainloop()

from database import get_all_analyses

data = get_all_analyses()
print(f"Total records: {len(data)}")

for r in data:
    print(f"ID:{r['id']} | File:{r['filename']} | Score:{r['final_score']}% | Date:{r['created_at']}")
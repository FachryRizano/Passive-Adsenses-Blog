import people_also_ask
def get_kw(keyword,total=12):
  questions = people_also_ask.get_related_questions(keyword,total)
  questions = [q.split("?")[0]+" ?" for q in questions]
  return questions
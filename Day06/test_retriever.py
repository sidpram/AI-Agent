from retriever import load_documents, retrieve

# documents = load_documents()
# print("--"*40)
# for doc in documents:
#     print(doc)
#     print(documents[doc])
#     print("--"*40)
# #print(load_documents())


file, content = retrieve("python")
print(file)
print(content)

file, content = retrieve("weather")
print(file)
print(content)
from app.ai.rag.rag_service import answer_question

if __name__ == "__main__":
    question = (
        "What cashback do Gold customers receive?"
    )
    
    response = answer_question(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(response['answer'])
    
    print("\nSources:")
    for source in response["sources"]:
        print("-", source)
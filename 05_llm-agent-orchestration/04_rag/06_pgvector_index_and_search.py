"""문서를 Ollama로 Embedding하여 pgvector에 저장하고 검색합니다."""

from _pgvector_store import delete_collection, similarity_search, upsert_text


COLLECTION = "rag_lesson"
DOCUMENTS = [
    # ("호텔 환불", "체크인 3일 전까지 취소하면 전액 환불합니다.", "hotel-refund.md"),
    # ("호텔 환불", "당일 취소는 환불되지 않습니다.", "hotel-refund.md"),
    # ("수하물", "교육용 국내선의 위탁 수하물은 15kg까지 허용합니다.", "baggage.md"),
    # ("관광지", "바다 박물관은 매주 화요일에 휴관합니다.", "attraction-hours.md"),
    # ("호텔 체크인아웃", "호텔 체크인은 오후3시이고, 호텔 체크아웃은 오전11시까지입니다.", "hotel_checkinout.md"),
    # ("regal", "임처인은 최대한 권한을 보호받는다.", "regal.md"),
    # ("regal", "임처인은 2년간의 기간을 보호받으며 이후 임대인과 협의 후 연장 가능 하다.", "regal.md"),
    ("상품 정보", "상품의 사이즈표를 기준으로 안내해 드릴게요. 평소 착용하는 사이즈나 키와 체형 정보를 알려주시면 참고 사이즈도 추천해 드릴 수 있어요.","information.md"),
    ("배송", "주문 상품의 현재 배송 상태와 예상 도착일(2~3일)을 확인해 드릴게요. 지역이나 택배사 사정에 따라 실제 도착일은 달라질 수 있습니다.","shipping.md"),
    ("취소,교환,환불", "결제 완료 후 상품이 상품 준비중인 상태라면 바로 취소할 수 있습니다. 이미 배송이 시작됐다면 반품 절차로 진행해야 할 수 있어요.","cancle-refund.md"),
    ("취소,교환,환불", "반품 상품 확인이 완료된 후 결제 수단에 따라 환불됩니다. 카드 결제는 카드사 처리 과정 때문에 추가로 며칠이 걸릴 수 있어요.","cancle-refund.md"),

]


def index_documents() -> None:
    delete_collection(COLLECTION)
    for index, (title, content, source) in enumerate(DOCUMENTS):
        upsert_text(
            collection=COLLECTION,
            title=title,
            content=content,
            source=source,
            chunk_index=index,
            metadata={"lesson": "04_rag"},
        )
        print(f"저장: {source} | {content}")


if __name__ == "__main__":
    index_documents()

    question = "상품을 언제 받을 수 있을까요?"
    print("\n질문:", question)
    for item in similarity_search(question, collection=COLLECTION, top_k=3):
        print(f"{item['score']:.3f} | {item['source']} | {item['content']}")

from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer("all-MiniLM-L6-v2")

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

username="neo4j"
password="password"
url = "bolt://localhost:7687"
database = "newmanash"
index_name = "edge-embedding"

graph = Neo4jGraph(url=url, username=username, password=password)

graph.refresh_schema()

print(graph.schema)
embeddings = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
query="Manash Kumar has how much family income?"
# top_k = 3
# index_name = "edge-embedding"
# query_embedding = embeddings.embed_query(query)
# print(query_embedding)
dimension = 384

# kg = Neo4jVector.from_existing_index(
#         embedding=embeddings,
#         url=url,
#         username=username,
#         password=password,
#         database="neo4j",  # neo4j by default
#         index_name="node-embedding",  # vector by default
#         # text_node_property="content",  # text by default
#         retrieval_query="""
#     CALL db.index.vector.queryRelationships({index}, {top_k}, {query_embedding})
#             YIELD relationship as doc, score
#             WITH startNode(doc) AS node_1, properties(doc) AS edge, endNode(doc) AS node_2, score
#             WITH "node_1: " + toString(node_1.content) + ", edge: " + toString(edge.content) + ", node_2: " + toString(node_2.content) AS doc, score
#             WITH { content: doc, score: score} AS doc, score
#             RETURN doc{.content, .score}
#             ORDER BY score DESC LIMIT $top_k""",
#     )


edge_kg = Neo4jVector.from_existing_relationship_index(
        embedding=embeddings,
        url=url,
        username=username,
        password=password,
        database=database,  # neo4j by default
        index_name=index_name,  # vector by default
        # text_node_property="content",  # text by default
        retrieval_query="""
            WITH relationship as doc, score
            WITH startNode(doc) AS node_1, properties(doc) AS edge, endNode(doc) AS node_2, score
            WITH "node_1: " + toString(node_1.content) + ", edge: " + toString(edge.content) + ", node_2: " + toString(node_2.content) AS doc, score
            RETURN doc as text, score
            """,
    )


# db = Neo4jVector.from_documents(
#     docs, OpenAIEmbeddings(), url=url, username=username, password=password
# )

# node_kg = Neo4jGraph.from_existing_index(
#         embedding=embeddings,
#         url=url,
#         username=username,
#         password=password,
#         database="neo4j",  # neo4j by default
#         index_name="node-embedding",  # vector by default
#         # text_node_property="body",  # text by default
#         retrieval_query="""
#     WITH node AS question, score AS similarity
#     CALL  { with question
#         MATCH (question)<-[:ANSWERS]-(answer)
#         WITH answer
#         ORDER BY answer.is_accepted DESC, answer.score DESC
#         WITH collect(answer)[..2] as answers
#         RETURN reduce(str='', answer IN answers | str + 
#                 '\n### Answer (Accepted: '+ answer.is_accepted +
#                 ' Score: ' + answer.score+ '): '+  answer.body + '\n') as answerTexts
#     } 
#     RETURN '##Question: ' + question.title + '\n' + question.body + '\n' 
#         + answerTexts AS text, similarity as score, {source: question.link} AS metadata
#     ORDER BY similarity ASC // so that best answers are the last
#     """,
#     )

docs_with_score = edge_kg.similarity_search_with_score(query, k=4)

context = ''
for i in docs_with_score:
    if i[1] > 0.5:
        context = context + i[0].page_content + "\n"

print(context)
print('\n\n')


# retriever = docs_with_score.as_retriever()

# qa = RetrievalQA.from_chain_type(llm = OpenAI(),
#                                  chain_type="stuff",
#                                  retriever=retriever)
# print(kg.embedding)
# print(kg.index_name)


llm = ChatGroq(temperature=0, groq_api_key="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" , model_name="mixtral-8x7b-32768")

system = "Give very accurate answer based on the given context. Don't make up answer if you don't know it."
human = ("Answer the following question based on the following context:\n Question: {query}\n context:"
                 "{context}")

prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | llm
ans = chain.invoke({"context": context, "query": query})

print(ans.content)




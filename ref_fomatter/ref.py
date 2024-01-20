import bibtexparser

idx=1

def format_citation(entry):
    global idx
    citation=""
    # print(entry,entry.get('ENTRYTYPE', ''))
    if entry.get('ENTRYTYPE', '') == 'misc':
#          @misc{webassembly,
#  title = {WebAssembly: A Binary Instruction Format for a Stack-based Virtual Machine},
#  howpublished = {\url{https://webassembly.org/}},
#  year = {Accessed: Nov. 15, 2023},
# }
        title=entry.get('title', '')
        if title[0]=='{':
            title=title[1:-1]
        url=entry.get('howpublished', '')[5:-1]
        time=entry.get('year', '')
        if time=="":
            time=entry.get('note', '')
        citation=f"{title}. {url}."
    else:
        authors = entry.get('author', '').split(' and ')
        first_author = authors[0].split(',')[0]
        conf=entry.get('booktitle', '')
        if conf=="":
            conf=entry.get('journal', '')
        # remove prefix year if exists
        if conf.find("20")==0:
            conf=conf[4:]
        # remove space at begining
        if conf.find(" ")==0:
            conf=conf[1:]
        
        print(conf)

        pages=entry.get('pages', '')
        if pages!="":
            pages=pages.replace("--","-")
            pages="; " + pages

        #remove \n , in authors[0]
        
        authors_conn=""
        author_idx=0
        for author in authors:
            def remove_n_comma(author):
                out=author.split(",")
                final=""
                if len(out)==2:
                    final= out[1]+" "+out[0]
                else:
                    final= author
                return final.strip().replace("\n","").replace(" and","")
            author=remove_n_comma(author)
            if author_idx<len(authors)-2:
                authors_conn+=author+", "
            elif author_idx<len(authors)-1:
                authors_conn+=author+" "
            else:
                authors_conn+="and "+author
            author_idx+=1


        title=entry.get('title', '')
        # print(title,title.title())
        # to BigCamel
        title=title.title()
        title=title.replace("And","and")
        title=title.replace("Of","of")
        title=title.replace("In","in")
        title=title.replace("The","the")
        title=title.replace("With","with")
        title=title.replace("For","for")
        title=title.replace("By","by")
        title=title.replace("On ","on ")
        title=title.replace("At ","at ")
        title=title.replace("To ","to ")
        title=title.replace("From ","from ")
        


        citation = f"{authors_conn}. {title}. {conf}. {entry.get('year', '')}{pages}."
    while citation.find("..")!=-1:
        citation=citation.replace("..",".")
    idx+=1
    return citation

def generate_citation_list(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        bib_database = bibtexparser.load(file)

    citation_list = [format_citation(entry) for entry in bib_database.entries]
    return citation_list

# 例子
input_file = 'ref.bib'
citation_list = generate_citation_list(input_file)


# for citation in citation_list:
#     print(citation)

output=""
for citation in citation_list:
    output+=citation+"\n"
# write to file
with open('ref.txt', 'w', encoding='utf-8') as file:
    file.write(output)
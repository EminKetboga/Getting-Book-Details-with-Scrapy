import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    page_count = 0
    books_count = 1
    file = open("kitaplarvedetayları.txt","a",encoding="utf-8")
    start_urls = [
            "https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1&filter_in_stock=1&filter_in_stock=1&page=1"
    ]
        
    def parse(self, response):
        books_name = response.css("div.name.ellipsis a span::text").extract()
        author_name = response.css("div.author.compact.ellipsis a::text").extract()
        yayin_evi = response.css("div.publisher span a span::text").extract()
        
        i = 0
        while (i < 20 ):
            
            self.file.write("------------------------------\n")
            self.file.write(str(self.books_count) + ". Kitap Bilgileri \n")
            self.file.write("Kitap İsmi : " + books_name[i] + "\n")
            self.file.write("Kitabın Yazarı : " + author_name[i] + "\n")
            self.file.write("Yayın Evi : " + yayin_evi[i] + "\n")
            self.file.write("------------------------------\n")
            self.books_count += 1




            """yield {

                "name" : books_name[i],
                "author" : author_name[i],
                "yayin" : yayin_evi[i]

            }"""
            i += 1
        next_url = response.css("a.next::attr(href)").extract_first()
        self.page_count += 1
        if next_url is not None and self.page_count < 5:
            yield scrapy.Request(url=next_url,callback=self.parse)

        else:
            self.file.close()
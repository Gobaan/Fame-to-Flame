import sys, Link, store

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        for line in f:
            link = Link.Link(line)
            printlink.update()
            store.store_solr(link.entries)


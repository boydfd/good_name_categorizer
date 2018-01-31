import logging

import resources

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(filename)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)
    resources.category.persist_text()


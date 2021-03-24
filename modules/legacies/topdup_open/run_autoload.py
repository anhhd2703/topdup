from autoload_data.data_utils import read_data_from_source, handle_post, logger
from autoload_data._config import MAX_LOAD_TIME

from tqdm import tqdm

if __name__ == '__main__':
    post_nb = 0
    for i in tqdm(range(MAX_LOAD_TIME)):
        try:
            posts = read_data_from_source(data_source="rabbitmq")
            handle_post(posts)
            post_nb += len(posts)
        except Exception as e:
            logger.exception(e)
            break
    logger.debug(f'Number of post: {post_nb}')

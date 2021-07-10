import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(file_name):
    logger.info('Transform process starting.')

    df = read_data(file_name)

    df = fill_missing_matchdays(df)

    df = add_total_goals(df)

    df['name'] = df['name'].apply(clear_value)

    df = add_average_column(df)

    df = add_scores_every_column(df)

    save_csv(df, file_name)


def read_data(file_name):
    logger.info(f'Processing file {file_name}')

    return pd.read_csv(file_name, encoding='utf-8')


def fill_missing_matchdays(df):
    logger.info(f'Filling missing match days.')
    return df.fillna(value=0)


def add_total_goals(df):
    logger.info(f'Adding Total Scores column.')
    columns = df.loc[:, 'J-1': 'J-17']
    df['total scores'] = columns.sum(numeric_only=True, axis=1)

    return df


def clear_value(value):
    logger.info(f'Cleaning Name column.')
    return value.replace("G - ", "")


def add_average_column(df):
    logger.info(f'Adding Scores Per Match column.')
    columns = df.loc[:, 'J-1': 'J-17']
    df['scores per match'] = columns.mean(numeric_only=True, axis=1)
    return df


def add_scores_every_column(df):
    logger.info(f'Adding Scores Every column.')
    df['scores every'] = df['minutes played']/df['total scores']
    return df


def save_csv(df, filename):
    clean_filename = f'clean_{filename}'
    logger.info(f'Saving new file: {clean_filename}')

    df.to_csv(clean_filename, index=False)


def run():
    main('top_scorers.csv')


if __name__ == '__main__':
    run()

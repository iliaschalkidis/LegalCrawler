import click
import crawlers
cli = click.Group()


@cli.command()
@click.option('--corpus', default='uk')
def download(corpus):

    if corpus == 'uk':
        crawlers.download_uk_legislation.download_uk_law()
    elif corpus == 'ja':
        crawlers.download_jap_legislation.download_ja_law()
    elif corpus == 'fin':
        crawlers.download_fin_legislation.download_fin_law()
    elif corpus == 'eu':
        crawlers.download_eu_legislation.download_eu_law()
    elif corpus == 'ca':
        crawlers.download_ca_legislation.download_ca_law()
    elif corpus == 'us':
        crawlers.download_us_case_law.download_us_caselaw()
    else:
        crawlers.download_uk_legislation.download_uk_law()
        crawlers.download_jap_legislation.download_ja_law()
        crawlers.download_fin_legislation.download_fin_law()
        crawlers.download_eu_legislation.download_eu_law()
        crawlers.download_ca_legislation.download_ca_law()
        crawlers.download_us_case_law.download_us_caselaw()

if __name__ == '__main__':
    download()

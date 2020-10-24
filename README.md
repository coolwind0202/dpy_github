# dpy_github
Discordのサーバー設定変更をGitHub上で差分確認できるようにするPythonパッケージ

# installation

以下をコマンドラインで実行してください。

```
pip install git+https://github.com/coolwind0202/dpy_github
```

# usage

## GitHubのトークンを生成

このライブラリのデフォルトの実装ではGitHubアクセストークンを使用します。
https://docs.github.com/ja/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token#%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%81%AE%E4%BD%9C%E6%88%90 を参考にGitHubのアクセストークンを生成できます（トークンのScopeは `Repo` のみで構いません。）

## コーディング

Discord.pyを使用してDiscord側の実装を行います。

```py
import discord
from discord.ext import commands
import dpy_github

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

github_token = ""
discord_token = ""

@bot.command()
async def push(ctx, *, commit_title):
    reporter = dpy_github.Reporter(guild=ctx.guild, github_token=github_token, 
        repository_name=f"log-{ctx.guild.id}", allow_new_repository=True)
    url = reporter.push(commit_title=commit_title)
    await ctx.send("記録が完了しました：" + url)

bot.run(discord_token)
```

GitHubのアクセストークン、DiscordBotのトークン共に、インターネット上で公開することのないようにしてください（このコードはあくまで使用方法の紹介を目的としています。）

```py
reporter = dpy_github.Reporter()
```

が、Discordサーバーの情報を記録するためのクラスになります。
guild引数に記録したいサーバー（discord.Guild）、github_tokenに先ほど取得したようなGitHubのアクセストークン、repository_nameには記録先のリポジトリ名を指定してください。
これらの引数は Reporter() インスタンスを生成する際に必須になります。

なお、allow_new_repository は「もし repository_name と同名のリポジトリが見つからなければ repository_name という名前で新しくリポジトリを新規作成するか」です。もしTrueであれば新規作成を許可します。

```py
url = reporter.push()
```

で実際にサーバー情報を記録します。正常に完了すると、リポジトリのGitHub上でのURLが返却されます。
commit_title引数を渡すと、その内容をメッセージとして使用しコミットを作成します。もし渡されなければ「commit」という文字列がデフォルトで使用されます。

下記のリンクはこのコードで生成されたコミットの差分表示の一例です。

https://github.com/coolwind0202/log-769408235731157024/commit/b46ea2d0544c520791b2f32e7a963f7d0368c8ba

また、リポジトリの構成は以下のようになります。
https://github.com/coolwind0202/log-769408235731157024

各ファイル名には正確性を期すためオブジェクトのIDが利用されていますが、これでは分かりにくいため index.md というファイルに目次が自動生成されます。

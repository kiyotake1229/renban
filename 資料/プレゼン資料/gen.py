# レンバン プレゼン資料（10枚）の生成。アプリ index.html のトークンをそのまま使う
# Python 3.9 のため f-string を入れ子にしない（部品を先に変数へ）
import json, os
OUT = os.path.dirname(os.path.abspath(__file__))

HEAD = '''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=BIZ+UDPGothic:wght@400;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    body { margin: 0; background: #121019; color: #F1EEF7; font-family: "BIZ UDPGothic", "Hiragino Sans", "Noto Sans JP", sans-serif; -webkit-font-smoothing: antialiased; }
    a { color: #FFB547; } a:hover { color: #FF5D9E; }
    .fd { font-family: "Bricolage Grotesque", "BIZ UDPGothic", "Hiragino Sans", sans-serif; }
    .fm { font-family: "IBM Plex Mono", "SFMono-Regular", Menlo, monospace; font-variant-numeric: tabular-nums; }
    .ico { width: 24px; height: 24px; stroke: currentColor; fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; flex: none; }
    .stub::before, .stub::after { content: ""; position: absolute; right: -10px; width: 20px; height: 20px; border-radius: 50%; background: #121019; }
    .stub::before { top: -10px; } .stub::after { bottom: -10px; }
  </style>
</helmet>
'''
TAIL = '''</x-dc>
</body>
</html>
'''

LIGHTS = ''.join('<i style="display:block;width:3px;height:%dpx;border-radius:2px;background:%s;box-shadow:0 0 8px %s"></i>' % (h, c, c)
                 for h, c in [(14, "#FF5D9E"), (18, "#FFB547"), (12, "#7FB0FF"), (16, "#4FD29B"), (14, "#FFB547"), (18, "#FF5D9E"), (12, "#7FB0FF")])

def slide(n, body, eyebrow, title, title_size=44):
    foot = ('<div style="position:absolute;left:64px;bottom:30px;display:flex;align-items:center;gap:14px">'
            '<span class="fm" style="font-size:13px;color:#7E789A;letter-spacing:.08em">No. %02d / 10</span>'
            '<span style="width:1px;height:14px;background:#2A2637"></span>'
            '<span class="fm" style="font-size:13px;color:#7E789A">レンバン · 社内提案 · 2026-09-14</span></div>'
            '<div style="position:absolute;right:64px;bottom:30px;display:flex;gap:10px;align-items:flex-end;height:18px">%s</div>') % (n, LIGHTS)
    head = ''
    if title:
        head = ('<div style="display:flex;flex-direction:column;gap:8px">'
                '<div class="fm" style="font-size:13px;letter-spacing:.14em;color:#FFB547">%s</div>'
                '<h1 class="fd" style="margin:0;font-size:%dpx;font-weight:800;line-height:1.2;letter-spacing:-.01em;color:#F1EEF7;text-wrap:balance">%s</h1></div>') % (eyebrow, title_size, title)
    return HEAD + ('<div style="width:1280px;height:720px;position:relative;overflow:hidden;background:#121019;padding:56px 64px 72px;box-sizing:border-box;display:flex;flex-direction:column;gap:28px">'
                   '%s%s%s</div>\n') % (head, body, foot) + TAIL

def paper(inner, extra=''):
    return '<div style="background:#F5F0E4;color:#17151F;border-radius:12px;padding:24px 26px;display:flex;flex-direction:column;gap:10px;box-shadow:0 14px 34px rgba(0,0,0,.4);%s">%s</div>' % (extra, inner)

def card(inner, extra=''):
    return '<div style="background:#1A1826;border:1px solid #2A2637;border-radius:12px;padding:22px 24px;display:flex;flex-direction:column;gap:10px;%s">%s</div>' % (extra, inner)

def tag(text, color='#FFB547', bg='rgba(255,181,71,.14)', border=''):
    return '<span class="fm" style="display:inline-flex;font-size:13px;padding:5px 9px;border-radius:4px;background:%s;color:%s;%s">%s</span>' % (bg, color, border, text)

def head_row(icon, text, size=22, color='#F1EEF7'):
    return '<div style="display:flex;align-items:center;gap:10px;color:#FFB547">%s<span style="font-size:%dpx;font-weight:700;color:%s">%s</span></div>' % (icon, size, color, text)

def p(text, size=16, color='#B9B3CC', lh=1.8):
    return '<p style="margin:0;font-size:%spx;line-height:%s;color:%s">%s</p>' % (size, lh, color, text)

def grid(cols, items, gap=18):
    return '<div style="display:grid;grid-template-columns:repeat(%d,minmax(0,1fr));gap:%dpx;flex:1;align-content:start">%s</div>' % (cols, gap, ''.join(items))

def check_line(text):
    return '<div style="display:flex;gap:10px;align-items:flex-start;font-size:16px;line-height:1.7;color:#F1EEF7"><span style="color:#4FD29B;margin-top:2px">%s</span><span>%s</span></div>' % (ICON['check'], text)

ICON = {
 'ticket': '<svg class="ico" viewBox="0 0 24 24"><path d="M4 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4z"/><path d="M14 6v12" stroke-dasharray="2 3"/></svg>',
 'sliders': '<svg class="ico" viewBox="0 0 24 24"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg>',
 'users': '<svg class="ico" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="3"/><path d="M15.5 14.5a5 5 0 0 1 5.5 5.5"/></svg>',
 'shield': '<svg class="ico" viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
 'flag': '<svg class="ico" viewBox="0 0 24 24"><path d="M5 21V4h12l-2 4 2 4H5"/></svg>',
 'heart': '<svg class="ico" viewBox="0 0 24 24"><path d="M12 20s-7-4.6-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.4-7 10-7 10z"/></svg>',
 'yen': '<svg class="ico" viewBox="0 0 24 24"><path d="M7 4l5 7 5-7M12 11v9M8 14h8M8 17h8"/></svg>',
 'x': '<svg class="ico" viewBox="0 0 24 24" style="fill:currentColor;stroke:none"><path d="M17.5 3h3.1l-6.8 7.8L21.8 21h-6.3l-4.9-6.4L5 21H1.9l7.3-8.3L1.5 3h6.4l4.4 5.9zM16.4 19.2h1.7L6.7 4.7H4.9z"/></svg>',
 'book': '<svg class="ico" viewBox="0 0 24 24"><path d="M5 4h14v16l-3-2-4 2-4-2-3 2z"/><path d="M9 9h6M9 13h4"/></svg>',
 'clock': '<svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 3h6"/></svg>',
 'search': '<svg class="ico" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
 'alert': '<svg class="ico" viewBox="0 0 24 24"><path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/></svg>',
 'check': '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12l4 4L19 7"/></svg>',
 'bell': '<svg class="ico" viewBox="0 0 24 24"><path d="M6 16v-5a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/></svg>',
}

files = {}

# ---------- 01 表紙 ----------
stub = ('<div class="stub" style="position:relative;width:220px;flex:none;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:36px 16px;background:#EBE4D2;border-right:2px dashed #D6CEBA">'
        '<span class="fm" style="font-size:16px;letter-spacing:.16em;color:#5E5969">SEP</span>'
        '<span class="fd" style="font-size:112px;font-weight:800;line-height:1;letter-spacing:-.03em">14</span>'
        '<span class="fm" style="font-size:15px;color:#5E5969">2026 · 月曜</span></div>')
cover_body = ('<div style="flex:1;padding:44px 52px 40px;display:flex;flex-direction:column;gap:14px;min-width:0">'
              '<div class="fm" style="font-size:15px;letter-spacing:.1em;color:#5E5969">社内提案 · アプリ開発</div>'
              '<div style="display:flex;align-items:center;gap:18px"><span style="width:16px;height:16px;border-radius:50%;background:#FFB547;box-shadow:0 0 16px #FFB547;flex:none"></span>'
              '<span class="fd" style="font-size:96px;font-weight:800;line-height:1;letter-spacing:-.02em">レンバン</span></div>'
              '<div style="font-size:26px;font-weight:700;line-height:1.5;color:#17151F">ライブの連番相手を、公演と条件から探す</div>'
              '<div class="fm" style="display:flex;gap:28px;font-size:15px;color:#5E5969;border-top:1px dashed #D6CEBA;padding-top:16px;margin-top:6px">'
              '<span>DEMO v9.2</span><span>SINGLE HTML · OFFLINE</span><span>kiyotake1229.github.io/renban</span></div></div>')
cover = ('<div style="display:flex;align-items:center;justify-content:center;flex:1">'
         '<div style="position:relative;display:flex;width:1040px;background:#F5F0E4;color:#17151F;border-radius:16px;box-shadow:0 30px 70px rgba(0,0,0,.55);overflow:hidden">'
         '%s%s</div></div>') % (stub, cover_body)
files['Main.dc.html'] = slide(1, cover, '', '')

# ---------- 02 課題 ----------
pains = [
 ('search', '見つからない', '募集は X のタイムラインに流れて消える。ハッシュタグで探しても、公演・日程・枚数が揃った相手にたどり着くまで時間がかかる。'),
 ('alert', '怖い', '相手の素性が分からないまま会う。転売、ドタキャン、当日の連絡が取れない。特に女性は「同性で本人確認済みの人」と最初から絞りたい。'),
 ('clock', '毎回、手間', '枚数・席・受け渡し方法・集合場所を DM で一から確認する。成立しても当日の段取りは頭の中だけ。'),
]
items = [paper(head_row(ICON[i], t, 30, '#17151F').replace('font-weight:700', 'font-weight:800').replace('<span style="font-size:30px', '<span class="fd" style="font-size:30px') + p(d, 17, '#3B3746', 1.85), 'min-height:250px') for i, t, d in pains]
body = grid(3, items, 22) + '<div style="font-size:18px;color:#B9B3CC;line-height:1.7">連番したい人は多いのに、探す場所が「X の募集ツイート」しかない。そこに構造を持ち込む。</div>'
files['S02.dc.html'] = slide(2, body, '01 · 課題', '連番探しは、まだ X の海の中にある')

# ---------- 03 解決 ----------
steps = [
 ('ticket', '公演を選ぶ', '「さがす」で公演を見つけて「行く」にする。その公演に行く人だけが並ぶ。'),
 ('sliders', '条件で絞って申請', '18項目の条件で相手を絞り、申請を送る。届いた申請は承諾か見送り。'),
 ('users', '当日メモで段取り', '成立したらトークと当日メモ。集合場所・受け渡し・チェックリストを共有。'),
 ('heart', '終演後は「ありがとう」', '送り合ったありがとうが信頼スコアになり、参戦の記録が手帳に残る。'),
]
items = []
for k, (i, t, d) in enumerate(steps):
    items.append(card('<div class="fm" style="font-size:13px;letter-spacing:.14em;color:#FFB547">STEP %d</div>' % (k + 1) + head_row(ICON[i], t) + p(d), 'min-height:270px'))
body = grid(4, items) + ('<div style="display:flex;align-items:center;gap:16px;background:#F5F0E4;color:#17151F;border-radius:12px;padding:18px 26px">'
                         '<span class="fd" style="font-size:24px;font-weight:800">スワイプで人を選ぶアプリではない。</span>'
                         '<span style="font-size:17px;color:#5E5969">連番は「その公演に一緒に入る相手」を探す行為なので、公演が先、人が後。</span></div>')
files['S03.dc.html'] = slide(3, body, '02 · 解決', '公演を選んでから、人を探す')

# ---------- 04 差別化 ----------
groups = [
 ('相手について', ['性別', '年代（上限・下限）', '未成年除外', '本人確認', 'ファンクラブ', '参戦回数', '連番の経験', '連番初心者', '推し一致']),
 ('チケット', ['相手のチケット（持っている / 譲れる / なし）', '受け渡し方法（電子分配 / 手渡し）']),
 ('当日の過ごし方', ['物販', '声出し', '終演後', '遠征', 'ホテル', '車']),
]
left = '<div style="display:flex;flex-direction:column;gap:14px">'
for g, xs in groups:
    chips = ''.join('<span style="font-size:14px;padding:5px 10px;border-radius:6px;background:#1A1826;border:1px solid #3B3650;color:#B9B3CC">%s</span>' % x for x in xs)
    left += ('<div style="display:flex;flex-direction:column;gap:8px"><div class="fm" style="font-size:13px;letter-spacing:.12em;color:#FFB547">%s</div>'
             '<div style="display:flex;flex-wrap:wrap;gap:6px">%s</div></div>') % (g, chips)
left += '</div>'
person = ('<div style="position:relative;display:flex;gap:14px;padding:18px;background:#1A1826;border:1px solid #2A2637;border-radius:12px">'
          '<div class="fd" style="width:54px;height:54px;border-radius:50%%;background:hsl(330 42%% 40%%);color:#F5F0E4;display:grid;place-items:center;font-size:19px;font-weight:800;flex:none">RA</div>'
          '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:8px;padding-right:70px">'
          '<div style="display:flex;gap:8px;align-items:center"><b style="font-size:19px">ゆい</b><span style="font-size:14px;color:#B9B3CC">@ramune_yui · 20代前半 · 女性</span></div>'
          '<div class="fm" style="display:flex;gap:14px;font-size:14px;color:#B9B3CC"><span>参戦 <b style="color:#F1EEF7">31</b>回</span><span>連番 <b style="color:#F1EEF7">15</b>回</span><span>ありがとう <b style="color:#F1EEF7">27</b></span></div>'
          '<div style="display:flex;flex-wrap:wrap;gap:5px">'
          '<span style="font-size:13px;padding:4px 9px;border-radius:4px;background:rgba(255,93,158,.14);color:#FF5D9E">推し一致 ラムネ少女隊（なぎさ推し）</span>'
          '<span style="font-size:13px;padding:4px 9px;border-radius:4px;background:rgba(255,110,110,.14);color:#FF6E6E;text-decoration:line-through">遠征組</span>'
          '<span style="font-size:13px;padding:4px 9px;border-radius:4px;background:#242131;color:#B9B3CC">声出し全力</span>'
          '<span style="font-size:13px;padding:4px 9px;border-radius:4px;background:#242131;color:#B9B3CC">物販並ぶ</span></div>'
          '<div style="display:flex;justify-content:space-between;align-items:center;gap:8px">%s'
          '<span style="font-size:15px;font-weight:700;padding:9px 16px;border-radius:6px;background:#FFB547;color:#1C1300">連番を申請</span></div></div>'
          '<div style="position:absolute;top:18px;right:18px;text-align:right;line-height:1"><b class="fd" style="font-size:24px;font-weight:800;color:#FFB547">6/7</b><div style="font-size:11px;color:#7E789A;margin-top:3px">条件一致</div></div></div>'
          ) % tag('1枚持ち · 整理番号A 100番台', '#B9B3CC', 'transparent', 'border:1px solid #3B3650')
right = '<div style="display:flex;flex-direction:column;gap:14px">' + person + '<div style="display:flex;flex-direction:column;gap:8px">' + ''.join([
    check_line('条件を満たさない人も<b>一致率順</b>に見える。満たさない項目は打ち消し線。取りこぼさない'),
    check_line('標準の条件と、<b>公演ごとの条件</b>を分けて持てる'),
    check_line('条件を保存すると、合う人が新しく募集を始めたときに<b>お知らせ</b>'),
]) + '</div></div>'
body = '<div style="display:grid;grid-template-columns:480px minmax(0,1fr);gap:40px;flex:1;align-content:start">%s%s</div>' % (left, right)
files['S04.dc.html'] = slide(4, body, '03 · 差別化', '18項目の条件と、一致率で並ぶ相手')

# ---------- 05 安心 ----------
safe = [
 ('shield', '本人確認', '済みの人だけに絞れる。バッジは人物カードとシートに常時表示'),
 ('users', '同性のみ表示', '女性は初期値で ON。性別を「回答しない」の人には同性条件を適用しない'),
 ('flag', '通報・ブロック', '人物シートとチャットのメニューから。ブロックすると一覧・申請・トークから消える'),
 ('yen', '金銭はアプリ外・定価のみ', 'チケットの売買を扱わない設計。転売の場にしない（審査とリスクの両面）'),
 ('heart', 'ありがとうが信頼スコア', '終演後に送り合う。参戦回数・連番回数・ありがとう数が次の相手への信用になる'),
 ('book', '当日メモ', '集合場所・時間・受け渡し・連絡手段のチェックリスト。「会えない」を減らす'),
]
items = [card(head_row(ICON[i], t, 21) + p(d, 15.5), 'min-height:170px') for i, t, d in safe]
files['S05.dc.html'] = slide(5, grid(3, items), '04 · 安心設計', '安全を、あとから足すのではなく先に設計する')

# ---------- 06 日常化 ----------
cd_inner = ('<div class="fm" style="font-size:13px;letter-spacing:.12em;color:#5E5969">次の現場まで</div>'
            '<div style="display:flex;align-items:baseline;gap:10px"><span class="fd" style="font-size:96px;font-weight:800;line-height:.95;letter-spacing:-.04em;color:#E1931A">13</span><span style="font-size:22px;font-weight:700;color:#5E5969">日</span></div>'
            '<div class="fd" style="font-size:22px;font-weight:800">ラムネ少女隊 · Zepp Haneda</div>'
            '<div class="fm" style="font-size:14px;color:#5E5969;border-top:1px dashed #D6CEBA;padding-top:10px">OPEN 16:30 · START 17:30 · スタンディング</div>')
cd = paper(cd_inner, 'min-height:300px;justify-content:center')
sched_rows = ''
for d, t, k, c, b in [('16', '東京ドーム FC先行 申込締切', '締切', '#FF5D9E', 'rgba(255,93,158,.14)'), ('25', '東京ドーム FC先行 当落発表', '当落', '#FF5D9E', 'rgba(255,93,158,.14)'), ('26', 'さいたま・大阪 一般発売', '一般発売', '#FFB547', 'rgba(255,181,71,.14)'), ('23', 'アルバム「灯り」発売', 'リリース', '#B9B3CC', '#242131')]:
    sched_rows += '<div style="display:flex;gap:14px;align-items:center;padding:9px 0;border-bottom:1px solid #2A2637"><span class="fd" style="width:34px;font-size:20px;font-weight:800">%s</span><span style="flex:1;color:#F1EEF7">%s</span>%s</div>' % (d, t, tag(k, c, b))
sched = card(head_row(ICON['bell'], '推しの予定', 20) + '<div style="display:flex;flex-direction:column;font-size:15px">%s</div>' % sched_rows + '<div style="font-size:14px;color:#7E789A">先行締切・当落・リリース・配信・TV。締切3日以内は強調</div>', 'min-height:300px')
stats = ''.join('<div style="background:#242131;border-radius:8px;padding:10px;text-align:center"><b class="fd" style="display:block;font-size:26px;font-weight:800">%s</b><span style="font-size:12px;color:#B9B3CC">%s</span></div>' % (v, l) for v, l in [('5', '今年の参戦'), ('¥75,100', '記録した費用'), ('<span style="font-size:15px;line-height:1.3;display:block;padding:6px 0 4px">GLASS HORIZON</span>', 'いちばん行った推し')])
diary = card(head_row(ICON['book'], '手帳', 20) + '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px">%s</div>' % stats + p('満足度・席・連番相手・費用（チケット/交通/宿/物販）・セトリ感想。履歴は連番の実績として相手にも見える', 15, '#B9B3CC', 1.75), 'min-height:300px')
body = '<div style="display:grid;grid-template-columns:360px minmax(0,1fr) minmax(0,1fr);gap:20px;flex:1;align-content:start">%s%s%s</div>' % (cd, sched, diary)
body += '<div style="font-size:18px;color:#B9B3CC;line-height:1.7">連番が決まっていない日も開く理由をつくる。開く回数が増えるほど、募集に気づく速さが上がる。</div>'
files['S06.dc.html'] = slide(6, body, '05 · 日常化', '連番がない日も、毎日開くアプリにする')

# ---------- 07 X連携 ----------
xs = [
 ('投稿', '募集内容と条件を定型文にして X の投稿画面を開く。アプリの公演ページへの直リンクとハッシュタグ入り。Web Intent なので API キー不要・無料'),
 ('取り込み', 'X の募集文を貼ると、公演・枚数・席・受け渡し・条件を自動で認識して参戦予定と条件に反映。乗り換えの手間をゼロにする'),
 ('連携表示', 'X アカウント連携済（フォロワー数・利用歴）を信頼の材料として表示。本番は「X でログイン」'),
]
items = [paper('<div style="display:flex;align-items:center;gap:10px">%s<span class="fd" style="font-size:28px;font-weight:800">%s</span></div>' % (ICON['x'], t) + p(d, 16.5, '#3B3746', 1.85), 'min-height:250px') for t, d in xs]
body = grid(3, items, 20) + ('<div style="display:flex;gap:24px;align-items:center">'
    '<div style="flex:1;font-size:18px;color:#B9B3CC;line-height:1.7">X をやめさせるのではなく、<b style="color:#F1EEF7">X に出して呼び込む</b>。募集を見た人がリンクから来ると、その募集ページに直接たどり着く。</div>'
    '<div style="font-size:14px;color:#7E789A;line-height:1.7;max-width:420px;border-left:1px solid #2A2637;padding-left:20px">X からの読み取り（ハッシュタグ監視など）は API が月 $200〜のため未実装。無料の範囲だけで成立させている。</div></div>')
files['S07.dc.html'] = slide(7, body, '06 · X 連携', 'X に出して、アプリに呼び込む')

# ---------- 08 デモの現状 ----------
done = ['公演検索（ジャンル・内容・時期・エリア・会場・募集状況）と保存した検索', '18項目の条件・一致率順・公演ごとの条件', '申請 → 承諾 → 成立 → トーク（既読・入力中・スタンプ）→ 当日メモ', '終演後の「ありがとう」→ 手帳に記録', 'カウントダウン・推しの予定・お知らせ', 'X 投稿・X 募集文の取り込み・連携表示', '通報・ブロック、同性のみ表示、性別と経験による初期設定', '初回の使い方案内、ペンライトの色（差し色）、ダーク／ライト']
left = '<div style="display:flex;flex-direction:column;gap:9px">' + ''.join(check_line(d) for d in done) + '</div>'
right = paper('<div class="fm" style="font-size:13px;letter-spacing:.12em;color:#5E5969">いま触れる</div>'
              '<div class="fd" style="font-size:22px;font-weight:800;line-height:1.3">kiyotake1229.github.io/renban/</div>'
              '<div style="font-size:15px;line-height:1.8;color:#3B3746">iPhone の Safari で開き、共有メニューから「ホーム画面に追加」。アイコンから全画面で起動し、オフラインでも動く。</div>'
              '<div class="fm" style="display:flex;flex-wrap:wrap;gap:8px;border-top:1px dashed #D6CEBA;padding-top:14px;font-size:13px;color:#5E5969"><span>単一 HTML</span><span>·</span><span>通信なし</span><span>·</span><span>端末内保存</span><span>·</span><span>架空データ 16人 / 21公演</span></div>', 'min-height:300px;justify-content:center')
body = '<div style="display:grid;grid-template-columns:minmax(0,1fr) 440px;gap:40px;flex:1;align-content:start">%s%s</div>' % (left, right)
files['S08.dc.html'] = slide(8, body, '07 · デモの現状', 'デモ版 v9.2 で、一連の流れを最後まで触れる')

# ---------- 09 収益 ----------
rows = [
 ('本人確認バッジ', '身分証確認で「本人確認済」表示。条件で「済みのみ」に絞る人が多いほど価値が上がる', '1回課金'),
 ('プレミアム', '条件の保存数・お知らせの優先配信・並び替えなど「探す側」の機能を強化', '月額'),
 ('遠征アフィリエイト', '手帳の費用欄と参戦予定から、会場近くのホテル・新幹線・高速バスを提案', '成果報酬'),
 ('公式・主催者向け', '公演の公式登録、FC 限定の連番募集枠、来場者の傾向データ（匿名）', '法人契約'),
 ('チケットサイト送客', '「チケットなし」の人に一般発売・公式リセールのリンクを出す', '送客'),
]
table = ('<div class="fm" style="display:grid;grid-template-columns:240px minmax(0,1fr) 130px;gap:20px;padding:0 20px 10px;font-size:12px;letter-spacing:.12em;color:#7E789A;border-bottom:1px solid #2A2637"><span>案</span><span>内容</span><span>形</span></div>')
for a, b, c in rows:
    table += '<div style="display:grid;grid-template-columns:240px minmax(0,1fr) 130px;gap:20px;align-items:center;padding:14px 20px;border-bottom:1px solid #2A2637"><span style="font-size:19px;font-weight:700">%s</span><span style="font-size:15.5px;line-height:1.7;color:#B9B3CC">%s</span><span>%s</span></div>' % (a, b, tag(c))
body = '<div style="display:flex;flex-direction:column;flex:1">%s</div>' % table
body += '<div style="font-size:17px;color:#B9B3CC;line-height:1.7">どれもユーザー間の金銭授受を挟まない。転売の場にならないことが、収益と審査の両方の前提。まずは無料アプリとして出し、本人確認バッジから試す。</div>'
files['S09.dc.html'] = slide(9, body, '08 · 収益モデルの仮説', '連番に特化しているから取れる導線')

# ---------- 10 次のステップ ----------
road = [
 ('1', 'Supabase 版', '認証・ユーザー DB・公演データ・申請とチャットのリアルタイム同期。無料枠で始める', '2〜4週間'),
 ('2', '審査対応', 'アカウント削除、規約への同意、Sign in with Apple、プライバシーポリシー、サポート URL', '1週間'),
 ('3', 'iOS 化', 'Capacitor で包み、プッシュ通知を追加。habit と同じ構成', '1週間'),
 ('4', '申請', '年齢制限 17+、「データを収集します」の申告、スクリーンショット3サイズ', '—'),
]
items = [card('<div class="fd" style="font-size:44px;font-weight:800;line-height:1;color:#FFB547">%s</div><div style="font-size:21px;font-weight:700">%s</div>%s<div class="fm" style="font-size:13px;color:#7E789A;border-top:1px solid #2A2637;padding-top:10px">目安 %s</div>' % (n, t, p(d, 15, '#B9B3CC', 1.75).replace('<p style="', '<p style="flex:1;'), w), 'min-height:280px') for n, t, d, w in road]
cost = paper('<div class="fm" style="font-size:12px;letter-spacing:.12em;color:#5E5969">費用</div><div style="display:flex;align-items:baseline;gap:10px"><span class="fd" style="font-size:36px;font-weight:800">¥12,800</span><span style="font-size:15px;color:#5E5969">/ 年 · Apple Developer Program のみ</span></div><div style="font-size:14px;color:#3B3746">Supabase・GitHub Pages・APNs・TestFlight は無料枠</div>', 'flex:1;padding:18px 24px;gap:6px')
decide = card('<div class="fm" style="font-size:12px;letter-spacing:.12em;color:#FFB547">今日決めたいこと</div><div style="font-size:18px;font-weight:700;line-height:1.6">Supabase 版に進むか。進むなら、公演データを最初は誰が登録するか。</div>', 'flex:1;padding:18px 24px;gap:6px;justify-content:center')
body = grid(4, items) + '<div style="display:flex;gap:20px">%s%s</div>' % (cost, decide)
files['S10.dc.html'] = slide(10, body, '09 · 次のステップ', '本番化への道と、今日決めたいこと')

for name, src in files.items():
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(src)

names = ['Main.dc.html'] + ['S%02d.dc.html' % i for i in range(2, 11)]
W, H, GX, GY = 1280, 720, 80, 140
boards = []
for i, f in enumerate(names):
    r, c = divmod(i, 5)
    boards.append({'file': f, 'x': c * (W + GX), 'y': r * (H + GY), 'w': W, 'h': H, 'title': '%02d' % (i + 1)})
json.dump({'artboards': boards, 'launch': {'view': 'focused', 'file': 'Main.dc.html'}}, open(os.path.join(OUT, 'canvas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', len(files))

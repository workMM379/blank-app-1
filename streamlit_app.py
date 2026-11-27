import streamlit as st

# ---------------------------------------------------------
# 1. ページ設定とカスタムCSS（薄い黄色マーカー風のスタイル）
# ---------------------------------------------------------
st.set_page_config(
    page_title="基礎看護技術 手順確認アプリ",
    page_icon="🩺",
    layout="wide",
)

st.markdown(
    """
    <style>
    /* 薄い黄色マーカー（蛍光ペン風） */
    .marker {
        background: linear-gradient(transparent 45%, #fff59d 45%);
        font-weight: 600;
        padding: 0 3px;
        border-radius: 2px;
    }
    /* 根拠・ポイント表示用の枠 */
    .point-box {
        background-color: #f8f9fa;
        border-left: 4px solid #fbc02d;
        padding: 10px 14px;
        margin-top: 6px;
        margin-bottom: 14px;
        border-radius: 0 6px 6px 0;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. 基礎看護技術データ（ここを編集・追加して内容を拡張できます）
#    重要箇所は <span class="marker">〜</span> で囲みます
# ---------------------------------------------------------
NURSING_PROCEDURES = [
    {
        "id": "hand_hygiene",
        "category": "感染予防",
        "title": "衛生的手洗い（流水と石けん）",
        "purpose": "手指に付着した通過菌や汚染物を物理的・化学的に除去し、交差感染を防止する。",
        "items": ["液体石けん", "ペーパータオル", "流水設備"],
        "steps": [
            {
                "step": "1. 準備",
                "action": "時計や指輪を外し、<span class='marker'>袖を肘の上までまくる</span>。爪が短く切られていることを確認する。",
                "rationale": "装飾品や長い爪の間には微生物が残留しやすく、洗浄不十分の原因になるため。",
            },
            {
                "step": "2. 予洗いと石けんの泡立て",
                "action": "流水で手を濡らしてから液体石けんを適量とり、<span class='marker'>手のひらで十分に泡立てる</span>。",
                "rationale": "先に手を濡らすことで石けんの界面活性作用が働きやすくなり、皮膚への刺激も軽減できる。",
            },
            {
                "step": "3. 洗い残しやすい部位の洗浄",
                "action": "手のひら・手の甲・指の間・<span class='marker'>親指の付け根（ねじり洗い）</span>・<span class='marker'>指先と爪の間</span>・手首の順に丁寧に洗う。",
                "rationale": "親指周り・指先・指間は最も洗い残しが多い部位であるため、意識的に擦り洗いを行う。",
            },
            {
                "step": "4. すすぎと乾燥",
                "action": "石けん分が残らないよう流水で十分にすすぎ、<span class='marker'>ペーパータオルで水気を完全に拭き取る</span>。",
                "rationale": "水分が残っていると細菌が繁殖しやすく、次に装着する手袋の破損にもつながる。",
            },
            {
                "step": "5. 蛇口の閉栓",
                "action": "手を拭いた<span class='marker'>使用済みのペーパータオルを使って蛇口を閉める</span>（自動水栓でない場合）。",
                "rationale": "洗浄後の清潔な手で汚染された蛇口に直接触れ、再汚染されるのを防ぐため。",
            },
        ],
    },
    {
        "id": "blood_pressure",
        "category": "バイタルサイン",
        "title": "血圧測定（上腕・聴診法）",
        "purpose": "循環動態を把握し、異常の早期発見や治療・ケアの評価を行う。",
        "items": ["水銀柱またはアネロイド血圧計", "聴診器", "アルコール綿"],
        "steps": [
            {
                "step": "1. 環境調整と安静の確保",
                "action": "患者に説明し、測定前に<span class='marker'>5〜10分程度の安静</span>を保つ。測定部位（上腕）が<span class='marker'>心臓の高さ</span>になるよう姿勢を整える。",
                "rationale": "運動や緊張直後は血圧が一過性に上昇する。また、上腕が心臓より低いと高く、高いと低く測定される。",
            },
            {
                "step": "2. マンシェットの装着",
                "action": "上腕動脈の拍動を触知し、ゴム嚢の中央が上腕動脈の真上にくるように巻く。下端は<span class='marker'>肘窩から2〜3cm上</span>とし、<span class='marker'>指が1〜2本入る程度</span>のゆとりを持たせる。",
                "rationale": "巻き方が緩すぎると実際より高い値に、きつすぎると低い値になるため。",
            },
            {
                "step": "3. 触診法による収縮期血圧の推定",
                "action": "橈骨動脈を触知しながら加圧し、拍動が消失した点から<span class='marker'>さらに20〜30mmHg加圧</span>して減圧し、再び拍動を触れた値を記憶する。",
                "rationale": "聴診間隙による誤測定を防ぎ、必要以上の加圧による患者の苦痛を避けるため。",
            },
            {
                "step": "4. 聴診法による測定",
                "action": "上腕動脈上に聴診器の膜型チェストピースを軽く当て、触診値より20〜30mmHg上まで加圧後、<span class='marker'>1拍動につき2〜3mmHgの速さ</span>で減圧する。",
                "rationale": "減圧が速すぎると正確な値を読み取れず、遅すぎると静脈うっ血を起こし拡張期血圧が高く出る。",
            },
            {
                "step": "5. 値の読み取りと後片付け",
                "action": "スワン第1点（音が聞こえ始めた点）を収縮期血圧、第5点（音が消失した点）を拡張期血圧として読み取り、<span class='marker'>速やかに空気を完全に抜いて</span>マンシェットを外す。",
                "rationale": "マンシェットを巻いたまま放置すると末梢の循環障害を引き起こすため。",
            },
        ],
    },
    {
        "id": "sterile_gloves",
        "category": "無菌操作",
        "title": "滅菌手袋の装着（オープン法）",
        "purpose": "無菌操作が必要な処置において、術者の手指からの微生物伝播を防ぎ清潔野を維持する。",
        "items": ["滅菌手袋（適切なサイズ）", "消毒用アルコール（事前手指衛生用）"],
        "steps": [
            {
                "step": "1. 外袋の開封と内袋の展開",
                "action": "手指衛生後、外袋を開封して乾いた清潔な台の上に内袋を置く。内袋の<span class='marker'>外側の端のみを持って</span>左右に開く。",
                "rationale": "内袋の内側は滅菌状態であるため、直接手指で触れて汚染させない。",
            },
            {
                "step": "2. 1枚目（利き手側）の装着",
                "action": "非利き手で手袋の<span class='marker'>折り返し部分の内側（皮膚に触れる面）</span>をつまみ持ち上げ、利き手を挿入する。",
                "rationale": "素手で触れてよいのは、装着後に自分の皮膚と接する「折り返しの内側」のみであるため。",
            },
            {
                "step": "3. 2枚目（非利き手側）の装着",
                "action": "滅菌手袋を着けた利き手の指を、2枚目の手袋の<span class='marker'>折り返し部分の外側（ポケット状の内側）</span>に差し入れて持ち上げ、非利き手を挿入する。",
                "rationale": "滅菌面同士（手袋の外側と折り返しの外側）を接触させることで無菌性を保つ。",
            },
            {
                "step": "4. フィット感の調整と姿勢の維持",
                "action": "滅菌面同士で指先のしわを伸ばし、装着後は手を<span class='marker'>腰より高く、肩より低い位置</span>で体の前に保つ。",
                "rationale": "腰より下や視界から外れる位置に手を下げると、不潔区域に触れて汚染されるリスクが高まるため。",
            },
        ],
    },
    {
        "id": "im_injection",
        "category": "与薬技術",
        "title": "筋肉内注射（中殿筋部位）",
        "purpose": "皮下組織より血流が豊富な筋層に薬液を注入し、確実かつ速やかな吸収を図る。",
        "items": ["薬液を吸った注射器", "注射針（21〜23G）", "アルコール綿", "未滅菌手袋", "針捨てボックス"],
        "steps": [
            {
                "step": "1. 患者確認と体位の調整",
                "action": "フルネーム・生年月日・薬剤名を照合する。腹臥位または側臥位にし、つま先を内側に向けるなどして<span class='marker'>殿筋を弛緩</span>させる。",
                "rationale": "筋肉が緊張した状態で刺入すると疼痛が強くなり、薬液の拡散も妨げられる。",
            },
            {
                "step": "2. 刺入部位の選定（クラークの点など）",
                "action": "<span class='marker'>上前腸骨棘と上後腸骨棘を結ぶ線の中点（またはクラークの点）</span>を確認し、坐骨神経や上殿動脈の走行を避けた安全な部位を選定する。",
                "rationale": "神経損傷や血管損傷による重篤な合併症（下肢麻痺・血腫など）を確実に防ぐため。",
            },
            {
                "step": "3. 消毒と皮膚の伸展",
                "action": "アルコール綿で中心から外側へ円を描くように消毒し、<span class='marker'>アルコールが完全に乾燥するのを待つ</span>。非利き手で刺入部の皮膚を伸展させる。",
                "rationale": "未乾燥のまま刺入するとアルコールが組織に入り激しい疼痛や組織刺激を起こす。",
            },
            {
                "step": "4. 刺入・逆血確認・薬液注入",
                "action": "皮膚に対して<span class='marker'>45〜90度の角度</span>で針を刺入し、しびれや激しい痛みがないか確認する。内筒を軽く引いて<span class='marker'>血液の逆流がないこと</span>を確認してからゆっくり注入する。",
                "rationale": "神経への接触や血管内への誤注入を防止するため。",
            },
            {
                "step": "5. 抜針と止血",
                "action": "刺入と同じ角度で素早く抜針し、アルコール綿で軽く押さえて止血する。<span class='marker'>リキャップはせず</span>直ちに針捨てボックスへ廃棄する。",
                "rationale": "針刺し切創事故を防止するため。なお、マッサージの可否は薬剤の特性（懸濁性製剤など）に従う。",
            },
        ],
    },
    {
        "id": "transfer_position",
        "category": "活動・休息援助",
        "title": "仰臥位から側臥位への体位変換",
        "purpose": "同一部位への圧迫を解除して褥瘡を予防し、安楽な姿勢保持や排痰・ケアを助ける。",
        "items": ["体位変換用クッション（2〜3個）", "バスタオル"],
        "steps": [
            {
                "step": "1. 環境整備とボディメカニクスの準備",
                "action": "ベッドの高さを<span class='marker'>看護師の腰の高さ</span>に調整し、ベッド柵を外す。看護師は足を前後に開いて<span class='marker'>支持基底面積を広げ、重心を低く</span>保つ。",
                "rationale": "看護師の腰痛予防と、安定した力の発揮のため。",
            },
            {
                "step": "2. 患者の基底面積の縮小",
                "action": "患者に説明した上で、<span class='marker'>両腕を胸の上で組み、両膝を立ててもらう</span>（介助が必要な場合は看護師が整える）。",
                "rationale": "身体を小さくまとめることでベッドとの摩擦面積が減り、少ない力で回転できるようになる。",
            },
            {
                "step": "3. 手前への水平移動と回転",
                "action": "向こう側へ回転させるスペースを作るため、一度患者を<span class='marker'>看護師側へ水平移動</span>させてから、肩と腰（大転子部）を支えて向こう側へ静かに回転させる。",
                "rationale": "ベッドの端に寄ってから回転させることで、体位変換後にベッド中央へ安定して収まる。",
            },
            {
                "step": "4. 良肢位の保持と除圧確認",
                "action": "下側になった肩と殿部を少し後ろへ引き抜いて圧迫を逃がす。背中・両膝の間・上側の腕の下にクッションを挿入し、<span class='marker'>骨突出部の圧迫や皮膚のねじれがないか</span>確認する。",
                "rationale": "下側の肩関節への過負荷や骨突出部への局所圧迫を防ぎ、安楽な姿勢を維持するため。",
            },
        ],
    },
]

# ---------------------------------------------------------
# 3. サイドバー：検索機能と手技選択
# ---------------------------------------------------------
st.sidebar.title("🩺 基礎看護技術ナビ")
st.sidebar.caption("手順・根拠・重要ポイントの確認用ツール")

# キーワード検索ボックス
search_query = st.sidebar.text_input(
    "🔍 キーワード検索",
    placeholder="例：逆血、クラーク、蛇口、心臓...",
    help="手技名、目的、手順、根拠の中の言葉を検索できます。",
)

# カテゴリー絞り込み
categories = ["すべて"] + sorted(list({p["category"] for p in NURSING_PROCEDURES}))
selected_category = st.sidebar.selectbox("📂 カテゴリーで絞り込み", categories)

# 検索条件に合う手技をフィルタリング
filtered_procedures = []
for proc in NURSING_PROCEDURES:
    if selected_category != "すべて" and proc["category"] != selected_category:
        continue

    if search_query.strip():
        q = search_query.strip().lower()
        # HTMLタグを除いた検索対象テキストを作成
        searchable_text = " ".join(
            [
                proc["title"],
                proc["category"],
                proc["purpose"],
                " ".join(proc["items"]),
                " ".join(
                    [
                        s["step"] + " " + s["action"] + " " + s["rationale"]
                        for s in proc["steps"]
                    ]
                ),
            ]
        ).lower()
        # 簡易的なタグ除去
        searchable_text = searchable_text.replace("<span class='marker'>", "").replace("</span>", "")
        if q not in searchable_text:
            continue

    filtered_procedures.append(proc)

st.sidebar.markdown("---")

# ---------------------------------------------------------
# 4. メイン画面の表示
# ---------------------------------------------------------
if not filtered_procedures:
    st.warning(f"「{search_query}」に一致する看護技術が見つかりませんでした。別のキーワードでお試しください。")
else:
    # 該当する手技から表示するものを選択
    procedure_titles = [f"【{p['category']}】{p['title']}" for p in filtered_procedures]
    selected_index = st.sidebar.radio(
        f"📋 該当する技術（{len(filtered_procedures)}件）",
        range(len(procedure_titles)),
        format_func=lambda i: procedure_titles[i],
    )

    current_proc = filtered_procedures[selected_index]

    # ヘッダー情報
    st.caption(f"カテゴリー：{current_proc['category']}")
    st.title(current_proc["title"])

    # 検索ヒット時のガイド表示
    if search_query.strip():
        st.info(f"🔍 検索キーワード：「**{search_query.strip()}**」で絞り込み中")

    # 目的と必要物品
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("🎯 目的")
        st.write(current_proc["purpose"])
    with col2:
        st.subheader("🧰 必要物品")
        st.write("・" + " ・".join(current_proc["items"]))

    st.markdown("---")
    st.subheader("📝 手順と重要ポイント")
    st.caption("※ チェックボックスは演習時の進捗確認にお使いいただけます。薄い黄色マーカーは特に重要なポイントです。")

    # 手順リストの表示
    for idx, step_data in enumerate(current_proc["steps"]):
        col_chk, col_body = st.columns([0.05, 0.95])
        with col_chk:
            st.checkbox("", key=f"{current_proc['id']}_step_{idx}")
        with col_body:
            st.markdown(f"**{step_data['step']}**")
            # 重要箇所に黄色マーカーを適用して表示
            st.markdown(step_data["action"], unsafe_allow_html=True)
            # 根拠・留意点
            st.markdown(
                f"<div class='point-box'>💡 <strong>根拠・留意点：</strong>{step_data['rationale']}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.caption("※ 本アプリの記載内容は一般的な基礎看護教育の標準手順をもとに作成したサンプルです。実際の臨地実習や臨床現場では、各施設・教育機関の最新プロトコルに従ってください。")

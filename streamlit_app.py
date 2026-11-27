import json
import altair as alt
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# 1. ページ設定
# ---------------------------------------------------------
st.set_page_config(
    page_title="基礎看護技術 手順確認アプリ",
    page_icon="🩺",
    layout="wide",
)

# ---------------------------------------------------------
# 2. 基礎看護技術データ（全15手技収録）
#    - category_reading / reading で「あいうえお順」に整列します
#    - 重要箇所は <span class='marker'>〜</span> で囲みます
# ---------------------------------------------------------
RAW_NURSING_PROCEDURES = [
    {
        "id": "hand_hygiene",
        "category": "感染予防",
        "category_reading": "かんせんよぼう",
        "title": "衛生的手洗い（流水と石けん）",
        "reading": "えいせいてきてあらい",
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
        "category_reading": "ばいたるさいん",
        "title": "血圧測定（上腕・聴診法）",
        "reading": "けつあつそくてい",
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
        "category_reading": "むきんそうさ",
        "title": "滅菌手袋の装着（オープン法）",
        "reading": "めっきんてぶくろのそうちゃく",
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
        "category_reading": "よやくぎじゅつ",
        "title": "筋肉内注射（中殿筋部位）",
        "reading": "きんにくないちゅうしゃ",
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
        "id": "iv_injection",
        "category": "与薬技術",
        "category_reading": "よやくぎじゅつ",
        "title": "静脈内注射（ワンショット静注）",
        "reading": "じょうみゃくないちゅうしゃ",
        "purpose": "薬液を直接静脈内に注入し、即時的かつ確実な薬効の発現を図る。",
        "items": [
            "薬液を吸った注射器",
            "注射針（21〜23G）または翼状針",
            "駆血帯",
            "アルコール綿",
            "未滅菌手袋",
            "止血用絆創膏",
            "針捨てボックス",
        ],
        "steps": [
            {
                "step": "1. 患者確認と穿刺血管の選定",
                "action": "フルネーム・生年月日・薬剤名・投与速度を照合する。穿刺予定部位から<span class='marker'>7〜10cm中枢側</span>に駆血帯を巻き、<span class='marker'>橈側皮静脈や正中皮静脈</span>など弾力があり直線的な静脈を選定する。",
                "rationale": "蛇行した血管や関節部の血管は穿刺・固定が難しく、薬液の血管外漏出を起こしやすいため。",
            },
            {
                "step": "2. 消毒と穿刺・逆血の確認",
                "action": "未滅菌手袋を装着し、アルコール綿で消毒して<span class='marker'>完全に乾燥させる</span>。皮膚を伸展させて<span class='marker'>15〜30度の角度</span>で穿刺し、外筒内の<span class='marker'>血液の逆流（逆血）</span>を確認する。",
                "rationale": "針先が確実に静脈内腔に入っていることを客観的に確認するため。",
            },
            {
                "step": "3. 駆血帯の解除と薬液の注入",
                "action": "逆血を確認したら針先が動かないよう固定したまま<span class='marker'>駆血帯を外し</span>、指示された速度で<span class='marker'>ゆっくり薬液を注入</span>する。",
                "rationale": "駆血帯を巻いたまま注入すると静脈内圧が過度に上昇し、血管破裂や薬液漏出・急激な血中濃度上昇を招くため。",
            },
            {
                "step": "4. 注入中の観察（血管外漏出・副作用）",
                "action": "注入中は刺入部の<span class='marker'>腫脹・発赤・疼痛（血管外漏出の徴候）</span>がないか、また顔色や気分不快など全身状態の急変がないか継続的に観察する。",
                "rationale": "薬液の血管外漏出による組織壊死や、アナフィラキシーなどの即時型副作用を早期に発見するため。",
            },
            {
                "step": "5. 抜針・止血と針の廃棄",
                "action": "注入終了後、アルコール綿を当てて静かに抜針し、<span class='marker'>5分程度しっかり圧迫止血</span>する。<span class='marker'>リキャップはせず</span>直ちに針捨てボックスへ廃棄する。",
                "rationale": "静脈からの出血・皮下血腫の形成を防ぎ、針刺し事故を防止するため。",
            },
        ],
    },
    {
        "id": "sc_injection",
        "category": "与薬技術",
        "category_reading": "よやくぎじゅつ",
        "title": "皮下注射（上腕伸側など）",
        "reading": "ひかちゅうしゃ",
        "purpose": "皮下組織に薬液を注入し、筋肉内注射よりも緩徐で持続的な吸収を図る。",
        "items": [
            "薬液を吸った注射器",
            "注射針（24〜27G）",
            "アルコール綿",
            "未滅菌手袋",
            "止血用絆創膏",
            "針捨てボックス",
        ],
        "steps": [
            {
                "step": "1. 患者確認と刺入部位の選定",
                "action": "フルネーム・生年月日・薬剤名を照合する。主に<span class='marker'>上腕外側（肩峰と肘頭を結ぶ線の下1/3の部位）</span>や腹部など、皮下脂肪が厚く神経・太い血管が少ない部位を選定する。",
                "rationale": "上腕外側の下1/3は橈骨神経が深部を走行しており、神経損傷のリスクが低いため。",
            },
            {
                "step": "2. 消毒と皮膚のつまみ上げ",
                "action": "未滅菌手袋を装着し、アルコール綿で消毒して<span class='marker'>完全に乾燥させる</span>。非利き手で刺入部位周辺の<span class='marker'>皮膚と皮下組織を厚くつまみ上げる</span>。",
                "rationale": "皮下組織と筋層を分離し、針先が誤って筋層へ深く刺入されるのを防ぐため。",
            },
            {
                "step": "3. 刺入と逆血確認・薬液注入",
                "action": "針の切り口を上にして皮膚に対して<span class='marker'>10〜30度の角度</span>で刺入する。つまんでいた手を離し、内筒を引いて<span class='marker'>血液の逆流がないこと</span>を確認してからゆっくり注入する。",
                "rationale": "角度が深すぎると筋肉内注射になり、吸収速度が想定より速まってしまうため。",
            },
            {
                "step": "4. 抜針・止血と針の廃棄",
                "action": "刺入と同じ角度で抜針し、アルコール綿で軽く押さえる（原則として強く揉まない）。<span class='marker'>リキャップはせず</span>直ちに針捨てボックスへ廃棄する。",
                "rationale": "インスリンやヘパリン等の薬剤では、マッサージにより吸収速度が急変したり皮下出血を起こしたりするため。",
            },
        ],
    },
    {
        "id": "transfer_position",
        "category": "活動・休息援助",
        "category_reading": "かつどうきゅうそくえんじょ",
        "title": "仰臥位から側臥位への体位変換",
        "reading": "ぎょうがいからそくがいへのたいいへんかん",
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
    {
        "id": "venipuncture",
        "category": "診療の補助",
        "category_reading": "しんりょうのほじょ",
        "title": "静脈血採血（真空採血管ホルダー法）",
        "reading": "じょうみゃくけつさいけつ",
        "purpose": "検査に必要な静脈血を安全・確実に採取し、溶血や神経損傷などの合併症を防止する。",
        "items": [
            "真空採血管ホルダー",
            "採血針（21〜23G）",
            "必要な採血管",
            "駆血帯",
            "アルコール綿",
            "未滅菌手袋",
            "止血用絆創膏",
            "針捨てボックス",
        ],
        "steps": [
            {
                "step": "1. 患者確認と穿刺血管の選定",
                "action": "フルネーム・生年月日・採血管ラベルを照合する。穿刺予定部位から<span class='marker'>7〜10cm中枢側</span>に駆血帯を巻き、<span class='marker'>橈側皮静脈または正中皮静脈</span>など弾力のある太い血管を選定する。",
                "rationale": "尺側皮静脈の深部には上腕動脈や正中神経が走行しており、誤穿刺や神経損傷のリスクが高いため避ける。",
            },
            {
                "step": "2. 消毒と皮膚の伸展",
                "action": "未滅菌手袋を装着し、アルコール綿で穿刺部位を消毒して<span class='marker'>完全に乾燥させる</span>。非利き手の母指で穿刺部の<span class='marker'>3〜5cm末梢側の皮膚を手前に引いて固定</span>する。",
                "rationale": "血管の逃避（ローリング）を防ぎ、一回の穿刺で確実に血管内へ針先を入れるため。",
            },
            {
                "step": "3. 穿刺と採血管の挿入",
                "action": "針の切り口を上にして皮膚に対して<span class='marker'>15〜30度の角度</span>で穿刺する。ホルダーを固定したまま採血管を奥まで押し込み、規定量の血液が採取されるのを確認する。",
                "rationale": "角度が深すぎると血管後壁を突き抜けて血腫の原因になり、浅すぎると血管内に入らない。",
            },
            {
                "step": "4. 駆血帯の解除と抜針・止血",
                "action": "最後の採血管をホルダーから抜いた後、<span class='marker'>針を抜く前に必ず駆血帯を外す</span>。アルコール綿を当てて針を抜き、<span class='marker'>5分程度しっかり圧迫止血</span>する（揉まない）。",
                "rationale": "駆血帯を巻いたまま抜針すると静脈圧が高い状態で針孔が開き、皮下出血・血腫の原因になる。",
            },
            {
                "step": "5. 針の廃棄と検体の混和",
                "action": "<span class='marker'>リキャップせず</span>安全装置を作動させて直ちに針捨てボックスへ廃棄する。抗凝固剤入りの採血管は<span class='marker'>ゆっくり転倒混和（5〜8回）</span>する。",
                "rationale": "激しく振ると赤血球が破壊（溶血）され、カリウム値などの検査データが不正確になるため。",
            },
        ],
    },
    {
        "id": "urinary_catheterization",
        "category": "排泄援助",
        "category_reading": "はいせつえんじょ",
        "title": "一時的導尿（女性患者）",
        "reading": "いちじてきどうにょう",
        "purpose": "尿閉の解除や無菌的な検査尿の採取のため、尿道口から膀胱へカテーテルを挿入して排尿させる。",
        "items": [
            "滅菌ネラトンカテーテル（12〜14Fr）",
            "滅菌手袋",
            "滅菌鑷子（せっし）",
            "消毒綿球（0.02〜0.05%ベンザルコニウム塩化物など）",
            "滅菌潤滑剤",
            "膿盆・採尿器",
            "処置用シーツ",
        ],
        "steps": [
            {
                "step": "1. プライバシーの保護と体位の調整",
                "action": "カーテンを閉め、処置用シーツを敷く。仰臥位で膝を立てて両脚を広げてもらい（<span class='marker'>仰臥位屈膝位</span>）、露出を最小限にする。",
                "rationale": "羞恥心に配慮しつつ、外尿道口を明視できる体位を確保するため。",
            },
            {
                "step": "2. 滅菌物品の準備と滅菌手袋の装着",
                "action": "滅菌手袋を装着し、カテーテルの先端から<span class='marker'>約4〜5cm</span>に滅菌潤滑剤を塗布する。",
                "rationale": "尿道粘膜との摩擦を軽減し、疼痛や粘膜損傷を防ぐため。",
            },
            {
                "step": "3. 外陰部の消毒",
                "action": "非利き手で陰唇を開いて固定し、利き手の鑷子で消毒綿球を持ち、<span class='marker'>恥骨側から肛門側（上から下）へ一方向</span>に大陰唇・小陰唇・外尿道口の順に消毒する。",
                "rationale": "肛門側の常在菌が外尿道口へ持ち込まれるのを防ぐため、一度拭いた綿球は戻さず交換する。",
            },
            {
                "step": "4. カテーテルの挿入と排尿確認",
                "action": "固定している非利き手は離さずに外尿道口を確認し、カテーテルを<span class='marker'>4〜6cm挿入</span>する。尿の流出を確認したら<span class='marker'>さらに1〜2cm進め</span>、末端を膿盆へ向ける。",
                "rationale": "女性は尿道が短く（約3〜4cm）、膣口へ誤挿入しやすいため、視認したまま確実に挿入する。",
            },
            {
                "step": "5. 抜去と後片付け",
                "action": "尿の流出が止まったら下腹部を軽く押して残尿を出し切り、カテーテルの<span class='marker'>末端を折り曲げて（またはつまんで）</span>静かに抜去する。",
                "rationale": "抜去時にカテーテル内の残尿が滴下してシーツや皮膚を汚染するのを防ぐため。",
            },
        ],
    },
    {
        "id": "tube_feeding",
        "category": "栄養援助",
        "category_reading": "えいようえんじょ",
        "title": "経鼻胃管からの経管栄養法（注入の手順）",
        "reading": "けいびいかんからのけいかんえいようほう",
        "purpose": "経口摂取が困難な患者に対し、胃内に留置されたカテーテルから安全に栄養剤・水分を投与する。",
        "items": [
            "栄養剤（人肌程度に温めたもの）",
            "注入ボトル・イルリガートル",
            "カテーテルチップシリンジ（50mL）",
            "聴診器",
            "微温湯（白湯）",
            "pH試験紙（施設基準による）",
        ],
        "steps": [
            {
                "step": "1. 体位の調整（ファーラー位）",
                "action": "禁忌がなければベッドの頭側を<span class='marker'>30〜45度（半座位・ファーラー位）</span>に挙上する。",
                "rationale": "食道への逆流および誤嚥性肺炎を防止するため。",
            },
            {
                "step": "2. 胃管の留置位置の確認（最重要）",
                "action": "鼻翼部のマーキングのずれがないか確認し、シリンジで<span class='marker'>胃内容物を吸引して性状・pH（酸性）を確認</span>する。さらに空気を10〜20mL注入して<span class='marker'>心窩部で気泡音</span>を聴取する。",
                "rationale": "胃管が気管内に迷入している状態で栄養剤を注入すると、重篤な窒息や化学性肺炎を引き起こすため。",
            },
            {
                "step": "3. 胃内残量の確認",
                "action": "前回の栄養剤が多量に胃内に残っていないか吸引して確認する。残量が<span class='marker'>100mL以上</span>ある場合は注入を控え医師へ報告する。",
                "rationale": "消化管の蠕動低下による嘔吐・逆流を防ぐため。",
            },
            {
                "step": "4. 栄養剤の注入開始と観察",
                "action": "チューブのクレンメを閉じた状態でボトルと接続し、<span class='marker'>100mLあたり30〜60分程度</span>の速度で滴下を開始する。開始後5〜10分は悪心・腹痛・呼吸状態の変化がないか観察する。",
                "rationale": "急速な注入は下痢、腹部膨満、ダンピング症状、嘔吐の原因となるため。",
            },
            {
                "step": "5. フラッシュと注入後の体位保持",
                "action": "注入終了後、<span class='marker'>微温湯（白湯）20〜30mL</span>を注入してチューブ内を洗浄（フラッシュ）し、栓を閉じる。注入後も<span class='marker'>30〜60分間はファーラー位</span>を保つ。",
                "rationale": "チューブ内の栄養剤残留による閉塞や細菌繁殖を防ぎ、食後すぐの逆流を予防するため。",
            },
        ],
    },
    {
        "id": "bed_bath",
        "category": "清潔・衣生活援助",
        "category_reading": "せいけついせいかつえんじょ",
        "title": "全身清拭（ベッド上での清拭）",
        "reading": "ぜんしんせいしき",
        "purpose": "入浴できない患者の皮膚の汚れを除去して清潔を保ち、血行促進や爽快感をもたらすとともに皮膚状態を観察する。",
        "items": [
            "洗面器",
            "50〜55℃のお湯",
            "清拭用タオル（2〜3枚）",
            "バスタオル（2枚）",
            "保湿剤",
            "清潔な寝衣",
            "未滅菌手袋（陰部清拭用）",
        ],
        "steps": [
            {
                "step": "1. 環境調整と湯温の確認",
                "action": "室温を<span class='marker'>22〜26℃</span>に調整し、隙間風を防ぐ。洗面器に<span class='marker'>50〜55℃</span>のお湯を用意し、絞ったタオルの温度を看護師の手首の内側で確認する。",
                "rationale": "気化熱による体温低下（冷感）を防ぎ、熱傷を防止するため。",
            },
            {
                "step": "2. 清拭の基本原則（末梢から中枢へ）",
                "action": "タオルは指先が遊ばないよう<span class='marker'>ミトン巻き</span>にし、洗う部位以外はバスタオルで覆う。四肢は<span class='marker'>末梢から中枢（指先から心臓）に向かって</span>拭く。",
                "rationale": "静脈血やリンパ液の還流を促し、血行促進効果を高めるため。",
            },
            {
                "step": "3. 清拭の順序",
                "action": "①顔面（目頭から目尻へ）→ ②上肢 → ③胸部・腹部（<span class='marker'>腸の走行に沿った「の」の字</span>）→ ④背部（側臥位にして殿部まで）→ ⑤下肢 → ⑥陰部の順に拭く。",
                "rationale": "汚染の少ない部位から多い部位へと進めることで、感染や汚染の拡大を防ぐため。",
            },
            {
                "step": "4. 皮膚の観察と保湿・更衣",
                "action": "骨突出部の発赤（褥瘡の初期徴候）や皮膚の乾燥・剥離がないか観察する。水分を乾いたタオルで拭き取り、<span class='marker'>保湿剤を塗布</span>してから清潔な寝衣に着替えさせる。",
                "rationale": "皮膚のバリア機能を維持し、皮膚トラブルや褥瘡を予防するため。",
            },
        ],
    },
    {
        "id": "suctioning",
        "category": "呼吸・循環援助",
        "category_reading": "こきゅうじゅんかんえんじょ",
        "title": "口腔・鼻腔内吸引（一時的吸引）",
        "reading": "こうくうびくうないきゅういん",
        "purpose": "自力での喀痰排出が困難な患者の気道分泌物を除去し、気道開通と換気改善・誤嚥予防を図る。",
        "items": [
            "吸引器（吸引圧調整機能付き）",
            "吸引カテーテル（10〜14Fr）",
            "未滅菌手袋（または滅菌手袋）",
            "洗浄水（滅菌精製水または水道水）",
            "アルコール綿（または清浄綿）",
            "パルスオキシメーター",
        ],
        "steps": [
            {
                "step": "1. アセスメントと吸引圧の設定",
                "action": "呼吸音・SpO2・分泌物の貯留部位を確認する。吸引圧は成人で<span class='marker'>150〜200mmHg（20〜26kPa）以下</span>に設定する。",
                "rationale": "吸引圧が高すぎると気道粘膜の損傷や出血、無気肺を引き起こすため。",
            },
            {
                "step": "2. カテーテルの接続と無菌操作",
                "action": "手指衛生後、手袋を装着する。カテーテルの<span class='marker'>先端から10〜15cm</span>の挿入部分には直接触れないよう清潔に扱い、吸引チューブに接続する。",
                "rationale": "気道内へ細菌が持ち込まれることによる呼吸器感染症（肺炎など）を防ぐため。",
            },
            {
                "step": "3. カテーテルの挿入（陰圧をかけずに挿入）",
                "action": "吸引チューブの根元を折り曲げて<span class='marker'>陰圧をかけない状態</span>で、鼻腔からは下鼻道に沿って<span class='marker'>15〜20cm</span>（口腔からは10〜15cm）静かに挿入する。",
                "rationale": "陰圧をかけながら挿入すると、カテーテル先端が粘膜に吸着して損傷・出血を招くため。",
            },
            {
                "step": "4. 分泌物の吸引（1回10〜15秒以内）",
                "action": "折り曲げていたチューブを離して陰圧をかけ、カテーテルを<span class='marker'>指先で回転させながら引き抜く</span>。1回の吸引時間は<span class='marker'>10〜15秒以内</span>とする。",
                "rationale": "吸引中は気道内の酸素も同時に吸い出されるため、長時間の吸引は低酸素血症や不整脈を誘発する。",
            },
            {
                "step": "5. カテーテルの洗浄と観察",
                "action": "アルコール綿でカテーテルの外側を拭き、洗浄水を吸わせて内腔を洗い流す。吸引後の<span class='marker'>呼吸状態・SpO2の回復と痰の性状</span>を観察する。",
                "rationale": "カテーテル内の分泌物残留による閉塞や細菌繁殖を防ぎ、吸引効果を評価するため。",
            },
        ],
    },
    {
        "id": "oxygen_therapy",
        "category": "呼吸・循環援助",
        "category_reading": "こきゅうじゅんかんえんじょ",
        "title": "酸素吸入療法（鼻カニューレ・酸素マスク）",
        "reading": "さんそきゅうにゅうりょうほう",
        "purpose": "低酸素血症の改善や呼吸仕事量の軽減を図るため、適切な濃度・流量の酸素を安全に投与する。",
        "items": [
            "酸素配管（または酸素ボンベ）",
            "酸素流量計",
            "加湿瓶（滅菌精製水入り・4L/分以上等で必要な場合）",
            "鼻カニューレまたは酸素マスク",
            "パルスオキシメーター",
        ],
        "steps": [
            {
                "step": "1. 指示確認と火気厳禁の徹底",
                "action": "医師の指示（投与デバイス・酸素流量・目標SpO2）を確認する。周囲に<span class='marker'>火気や静電気の発生源がないこと</span>を確認する。",
                "rationale": "酸素は支燃性が強く、火気が近づくと激しい燃焼や火災・爆発の危険があるため。",
            },
            {
                "step": "2. 流量の調整と酸素流出の確認",
                "action": "流量計のフロート（浮き玉）の<span class='marker'>中心（または上端・機器仕様に従う）</span>を指示流量に合わせる。皮膚に当てる前に<span class='marker'>酸素が実際に出ていること</span>を確認する。",
                "rationale": "接続外れや流量計の閉塞による酸素未投与の事故を確実に防ぐため。",
            },
            {
                "step": "3. デバイスの装着と適切な流量管理",
                "action": "鼻カニューレはプロングの湾曲を鼻腔の向きに合わせて装着する。簡易酸素マスクを使用する場合は、呼気の再呼吸（CO2貯留）を防ぐため<span class='marker'>必ず5L/分以上</span>で投与する。",
                "rationale": "簡易酸素マスクで流量が5L/分未満になると、マスク内に呼気（二酸化炭素）が滞留し高炭酸ガス血症を招くため。",
            },
            {
                "step": "4. 皮膚トラブルの予防と観察",
                "action": "チューブが耳介や頬・鼻腔粘膜を強く圧迫していないか確認し、必要に応じて保護材を当てる。装着後は<span class='marker'>SpO2・呼吸数・意識レベル（CO2ナルコーシス徴候）</span>を観察する。",
                "rationale": "長時間の圧迫による医療関連機器圧迫創傷（MDRPU）や、COPD患者等でのCO2ナルコーシスを早期発見するため。",
            },
        ],
    },
    {
        "id": "oral_care",
        "category": "清潔・衣生活援助",
        "category_reading": "せいけついせいかつえんじょ",
        "title": "口腔ケア（誤嚥予防を意識したブラッシング）",
        "reading": "こうくうけあ",
        "purpose": "口腔内の細菌数を減少させて誤嚥性肺炎やう蝕・歯周病を予防し、味覚や咀嚼・嚥下機能の維持を図る。",
        "items": [
            "歯ブラシ（ヘッドが小さく軟らかいもの）",
            "スポンジブラシ",
            "ガーグルベースン（膿盆）",
            "コップ（微温湯）",
            "口腔保湿剤",
            "未滅菌手袋",
            "タオル・エプロン",
        ],
        "steps": [
            {
                "step": "1. 誤嚥防止の体位調整",
                "action": "意識レベルと嚥下機能を確認する。坐位またはファーラー位にし、<span class='marker'>顎を軽く引いた姿勢（頸部前屈位）</span>をとる。仰臥位の場合は<span class='marker'>顔を横向き</span>にする。",
                "rationale": "頸部が後屈していると気道が開き、唾液や洗浄水が気管へ流れ込みやすくなるため。",
            },
            {
                "step": "2. 歯ブラシによるブラッシング",
                "action": "ブラシの水分をよく切り、歯と歯肉の境目に<span class='marker'>45度の角度（バス法）</span>で毛先を当て、小刻みに動かしてプラーク（歯垢）を除去する。",
                "rationale": "歯周ポケット内の細菌を効率よく除去しつつ、歯肉への過度な刺激を避けるため。",
            },
            {
                "step": "3. 粘膜・舌の清掃（奥から手前へ）",
                "action": "水気をよく絞ったスポンジブラシで、頬粘膜・口蓋・舌の表面を<span class='marker'>奥から手前へ向かって</span>優しく拭き取る。",
                "rationale": "手前から奥へ動かすと汚れを咽頭側へ押し込み、誤嚥や嘔吐反射を誘発するため。",
            },
            {
                "step": "4. 含嗽（うがい）または拭き取りと保湿",
                "action": "うがいが可能な場合は少量の水で含嗽を促し、困難な場合は<span class='marker'>湿らせたガーゼやスポンジで汚れを回収</span>する。最後に<span class='marker'>口腔保湿剤</span>を薄く塗布する。",
                "rationale": "口腔内の乾燥は細菌の繁殖や粘膜損傷・口臭の原因となるため、保湿して粘膜を保護する。",
            },
        ],
    },
    {
        "id": "bed_making",
        "category": "環境整備",
        "category_reading": "かんきょうせいび",
        "title": "ベッドメーキング（臥床患者がいない場合）",
        "reading": "べっどめーきんぐ",
        "purpose": "しわやたるみのない清潔で快適な寝床を整え、褥瘡や皮膚トラブルを予防するとともに安眠を促す。",
        "items": [
            "敷布（シーツ）",
            "横シーツ（必要な場合）",
            "掛け布団・カバー",
            "枕・枕カバー",
        ],
        "steps": [
            {
                "step": "1. 環境整備とボディメカニクスの活用",
                "action": "マットレスの汚れを払い、上下を反転させる。ベッドの高さを<span class='marker'>看護師の腰の高さ</span>に調整し、足を前後に開いて重心を低く保つ。",
                "rationale": "マットレスの局所的なへたりを防ぎ、看護師の腰痛を予防するため。",
            },
            {
                "step": "2. シーツの敷き込みとコーナーの三角折り",
                "action": "シーツの中心線とマットレスの中心線を合わせて広げ、頭側の余りをマットレスの下へ深く折り込む。角は<span class='marker'>45度の角度で三角折り（エンベロープ法）</span>にして整える。",
                "rationale": "三角折りにすることでシーツが固定され、体動によって緩んだりしわができたりするのを防ぐため。",
            },
            {
                "step": "3. シーツの引き伸ばし（しわの防止）",
                "action": "足側・側面の順にシーツを強く引きながらマットレスの下へ折り込み、<span class='marker'>表面に一切のしわやたるみがない状態</span>に仕上げる。",
                "rationale": "シーツのしわは皮膚への局所的な圧迫や摩擦を生じさせ、褥瘡発生の直接的な原因となるため。",
            },
            {
                "step": "4. 掛け布団と枕の配置（足元のゆとり）",
                "action": "掛け布団は足元に<span class='marker'>タック（ひだ）を作る</span>などしてゆとりを持たせ、枕は縫い目が下や足側になるように配置する。",
                "rationale": "掛け布団の重みで足関節が底屈位に固定され、尖足（せんそく）変形を起こすのを防ぐため。",
            },
        ],
    },
]

# カテゴリー順・手技名（あいうえお順）にソート
NURSING_PROCEDURES = sorted(
    RAW_NURSING_PROCEDURES,
    key=lambda p: (p.get("category_reading", p["category"]), p.get("reading", p["title"])),
)

# ---------------------------------------------------------
# 3. 永続化処理（URLパラメータによる自動保存・復元）
# ---------------------------------------------------------
PROCEDURE_IDS = [p["id"] for p in NURSING_PROCEDURES]
PROCEDURE_MAP = {p["id"]: p for p in NURSING_PROCEDURES}


def load_counts_from_url() -> dict:
    """URLのクエリパラメータ（?c=id1:2,id2:1）から確認回数を復元する"""
    counts = {pid: 0 for pid in PROCEDURE_IDS}
    raw = st.query_params.get("c", "")
    if raw:
        for pair in raw.split(","):
            if ":" in pair:
                pid, val = pair.split(":", 1)
                if pid in counts and val.isdigit():
                    counts[pid] = int(val)
    return counts


def sync_counts_to_url(counts: dict):
    """0回より多い手技の回数をURLパラメータへ書き戻して永続化する"""
    pairs = [f"{pid}:{cnt}" for pid, cnt in counts.items() if cnt > 0]
    if pairs:
        st.query_params["c"] = ",".join(pairs)
    elif "c" in st.query_params:
        del st.query_params["c"]


if "review_counts" not in st.session_state:
    st.session_state.review_counts = load_counts_from_url()

for pid in PROCEDURE_IDS:
    if pid not in st.session_state.review_counts:
        st.session_state.review_counts[pid] = 0

# アプリ起動時は何も選択していない状態（None）にする
if "selected_proc_id" not in st.session_state:
    st.session_state.selected_proc_id = None

# 検索・絞り込み用のセッション状態初期化
if "search_query_input" not in st.session_state:
    st.session_state.search_query_input = ""

if "selected_category_input" not in st.session_state:
    st.session_state.selected_category_input = "すべて"


def clear_filters():
    """検索キーワードとカテゴリー絞り込みを初期状態に戻す"""
    st.session_state.search_query_input = ""
    st.session_state.selected_category_input = "すべて"


# ---------------------------------------------------------
# 4. サイドバー：暗記モード・検索機能・カテゴリー別手技一覧
# ---------------------------------------------------------
st.sidebar.title("🩺 基礎看護技術ナビ")
st.sidebar.caption("手順・根拠・重要ポイントの確認用ツール")

# 暗記モードの切り替えトグル
memorize_mode = st.sidebar.toggle(
    "🙈 暗記モード（重要箇所を隠す）",
    value=False,
    help="ONにすると黄色マーカー部分の文字が隠れます。隠れた部分にカーソルを合わせる（またはタップする）と個別に答えを確認できます。",
)

st.sidebar.markdown("---")

# キーワード検索ボックス
search_query = st.sidebar.text_input(
    "🔍 キーワード検索",
    key="search_query_input",
    placeholder="例：逆血、クラーク、吸引圧...",
    help="手技名、目的、手順、根拠の中の言葉を検索できます。",
)

# カテゴリー絞り込み（あいうえお順）
ordered_categories = []
for p in NURSING_PROCEDURES:
    if p["category"] not in ordered_categories:
        ordered_categories.append(p["category"])

selected_category = st.sidebar.selectbox(
    "📂 カテゴリーで絞り込み",
    ["すべて"] + ordered_categories,
    key="selected_category_input",
)

# 検索・絞り込みクリアボタン
is_filtered = bool(search_query.strip()) or (selected_category != "すべて")
st.sidebar.button(
    "🧹 検索・絞り込みをクリア",
    on_click=clear_filters,
    disabled=not is_filtered,
    use_container_width=True,
)

# ---------------------------------------------------------
# 5. カスタムCSS（通常モード／暗記モード／自分用チェックマーカー／ボタン調整）
# ---------------------------------------------------------
if memorize_mode:
    marker_css = """
    .marker {
        background-color: #fff176;
        color: transparent;
        border-bottom: 2px dashed #f57f17;
        padding: 1px 6px;
        border-radius: 4px;
        cursor: pointer;
        user-select: none;
        transition: color 0.15s ease, background-color 0.15s ease;
    }
    .marker:hover, .marker:active {
        color: #111111;
        background-color: #fff9c4;
    }
    """
else:
    marker_css = """
    .marker {
        background: linear-gradient(transparent 45%, #fff59d 45%);
        font-weight: 600;
        padding: 0 3px;
        border-radius: 2px;
    }
    """

st.markdown(
    f"""
    <style>
    {marker_css}
    /* 自分がチェックボックスを入れた手順に引く水色マーカー */
    .user-marker {{
        background: linear-gradient(transparent 45%, #b3e5fc 45%);
        padding: 0 3px;
        border-radius: 2px;
    }}
    .point-box {{
        background-color: #f8f9fa;
        border-left: 4px solid #fbc02d;
        padding: 10px 14px;
        margin-top: 6px;
        margin-bottom: 14px;
        border-radius: 0 6px 6px 0;
        font-size: 0.92rem;
    }}
    /* 確認回数表示枠（大きめ）と3つの操作ボタン（少しコンパクト）のサイズ調整 */
    .count-badge {{
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 44px;
        min-height: 44px;
        width: 100%;
        margin: 0;
        background-color: #e3f2fd;
        color: #0d47a1;
        font-weight: 700;
        padding: 0 12px;
        border-radius: 8px;
        font-size: 1.0rem;
        border: 1px solid #90caf9;
        white-space: nowrap;
    }}
    section[data-testid="stMain"] div[data-testid="stMarkdownContainer"]:has(.count-badge) {{
        margin: 0;
        padding: 0;
    }}
    section[data-testid="stMain"] div[data-testid="stMarkdownContainer"]:has(.count-badge) p {{
        margin: 0;
    }}
    /* 3つの操作ボタンは確認回数表示枠より一回り小さく揃える */
    section[data-testid="stMain"] button[kind="secondary"],
    section[data-testid="stMain"] button[kind="primary"] {{
        box-sizing: border-box;
        height: 36px;
        min-height: 36px;
        margin-top: 4px;
        border-radius: 6px;
        font-size: 0.86rem;
        white-space: nowrap;
        padding: 0 6px;
    }}
    /* サイドバー内の手技選択ボタンの左寄せ調整 */
    section[data-testid="stSidebar"] button[kind="secondary"],
    section[data-testid="stSidebar"] button[kind="primary"] {{
        justify-content: flex-start;
        text-align: left;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 6. 検索フィルタリングと折りたたみ式カテゴリー別手技リスト
# ---------------------------------------------------------
filtered_procedures = []
for proc in NURSING_PROCEDURES:
    if selected_category != "すべて" and proc["category"] != selected_category:
        continue

    if search_query.strip():
        q = search_query.strip().lower()
        searchable_text = " ".join(
            [
                proc["title"],
                proc.get("reading", ""),
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
        searchable_text = searchable_text.replace("<span class='marker'>", "").replace("</span>", "")
        if q not in searchable_text:
            continue

    filtered_procedures.append(proc)

current_proc = None
if filtered_procedures:
    filtered_ids = [p["id"] for p in filtered_procedures]

    # 選択中のIDが現在のフィルタ結果に含まれない場合は未選択（None）に戻す
    if (
        st.session_state.selected_proc_id is not None
        and st.session_state.selected_proc_id not in filtered_ids
    ):
        st.session_state.selected_proc_id = None

    # カテゴリーごとにグループ化（各カテゴリー内は既に「あいうえお順」）
    grouped_procs = {}
    for proc in filtered_procedures:
        grouped_procs.setdefault(proc["category"], []).append(proc)

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 📋 技術一覧（{len(filtered_procedures)}件）")
    st.sidebar.caption("※ カテゴリーをクリックで開閉できます（あいうえお順）")

    for cat_name, procs_in_cat in grouped_procs.items():
        # 選択中の手技が含まれるカテゴリー、または検索・絞り込み中は自動で展開する
        has_selected = any(p["id"] == st.session_state.selected_proc_id for p in procs_in_cat)
        is_expanded = has_selected or is_filtered

        with st.sidebar.expander(f"📂 {cat_name}（{len(procs_in_cat)}件）", expanded=is_expanded):
            for proc in procs_in_cat:
                pid = proc["id"]
                cnt = st.session_state.review_counts[pid]
                is_selected = pid == st.session_state.selected_proc_id
                prefix = "▶ " if is_selected else ""
                btn_label = f"{prefix}{proc['title']}（{cnt}回）"

                if st.button(
                    btn_label,
                    key=f"nav_btn_{pid}",
                    type="primary" if is_selected else "secondary",
                    use_container_width=True,
                ):
                    st.session_state.selected_proc_id = pid
                    st.rerun()

    if st.session_state.selected_proc_id is not None:
        current_proc = PROCEDURE_MAP[st.session_state.selected_proc_id]
else:
    st.session_state.selected_proc_id = None

# サイドバー下部：学習記録の保存ガイドとバックアップ機能
st.sidebar.markdown("---")
with st.sidebar.expander("💾 確認回数の保存・バックアップ"):
    st.caption(
        "確認回数はブラウザのURLに自動保存されます。このページをブックマークすると、ブラウザを閉じた後も続きから学習できます。"
    )
    backup_json = json.dumps(st.session_state.review_counts, ensure_ascii=False, indent=2)
    st.download_button(
        label="📥 記録をJSONで保存",
        data=backup_json,
        file_name="nursing_review_counts.json",
        mime="application/json",
        use_container_width=True,
    )
    uploaded_file = st.file_uploader("📤 JSONから復元", type=["json"])
    if uploaded_file is not None:
        try:
            loaded_data = json.load(uploaded_file)
            if isinstance(loaded_data, dict):
                for pid in PROCEDURE_IDS:
                    if pid in loaded_data and isinstance(loaded_data[pid], int):
                        st.session_state.review_counts[pid] = max(0, loaded_data[pid])
                sync_counts_to_url(st.session_state.review_counts)
                st.success("記録を復元しました！")
                st.rerun()
        except Exception:
            st.error("ファイルの読み込みに失敗しました。")

# ---------------------------------------------------------
# 7. メイン画面（タブ切り替え：手順の確認 ／ 確認回数グラフ）
# ---------------------------------------------------------
tab_procedure, tab_chart = st.tabs(["📖 手順の確認", "📊 確認回数グラフ"])

# === タブ1：手順の確認 ===
with tab_procedure:
    if not filtered_procedures:
        st.warning(
            f"「{search_query}」に一致する看護技術が見つかりませんでした。サイドバーの「🧹 検索・絞り込みをクリア」で解除できます。"
        )
    elif current_proc is None:
        st.title("🩺 基礎看護技術 手順確認アプリ")
        st.info("👈 左のサイドバー（スマホの場合は左上の「＞」アイコン）からカテゴリーを開き、確認したい基礎看護技術を選択してください。")
        st.markdown(
            """
            #### 💡 このアプリの使い方
            * **重要ポイントの確認**：薄い黄色マーカーは特に重要なポイントです。
            * **自分用マーキング**：各手順の左にあるチェックボックスを入れると、水色マーカーを引くことができます。
            * **暗記モード**：サイドバーの「🙈 暗記モード」をONにすると、黄色マーカー部分の文字を隠して学習できます。
            * **確認回数の記録**：手技を確認したら「✅ 確認完了（+1回）」で学習回数を記録し、「📊 確認回数グラフ」タブで進捗を振り返れます。
            """
        )
    else:
        proc_id = current_proc["id"]
        current_count = st.session_state.review_counts[proc_id]

        col_cat, col_close = st.columns([8, 2])
        with col_cat:
            st.caption(f"カテゴリー：{current_proc['category']}")
        with col_close:
            if st.button("✖ 選択を閉じる", key=f"close_{proc_id}", use_container_width=True):
                st.session_state.selected_proc_id = None
                st.rerun()

        st.title(current_proc["title"])

        # 確認回数の表示枠（大きめ）と3つの操作ボタン（少し小さめで統一）
        col_badge, col_add, col_sub, col_clear, _ = st.columns([2.3, 1.6, 1.6, 1.6, 1.9])
        with col_badge:
            st.markdown(
                f"<div class='count-badge'>👀 確認回数：{current_count} 回</div>",
                unsafe_allow_html=True,
            )
        with col_add:
            if st.button("✅ 確認完了（+1回）", key=f"add_{proc_id}", use_container_width=True):
                st.session_state.review_counts[proc_id] += 1
                sync_counts_to_url(st.session_state.review_counts)
                st.rerun()
        with col_sub:
            if st.button(
                "↩️ -1回",
                key=f"sub_{proc_id}",
                disabled=(current_count == 0),
                use_container_width=True,
            ):
                st.session_state.review_counts[proc_id] = max(0, current_count - 1)
                sync_counts_to_url(st.session_state.review_counts)
                st.rerun()
        with col_clear:
            if st.button(
                "🗑️ クリア（0回）",
                key=f"reset_{proc_id}",
                disabled=(current_count == 0),
                use_container_width=True,
            ):
                st.session_state.review_counts[proc_id] = 0
                sync_counts_to_url(st.session_state.review_counts)
                st.rerun()

        st.write("")

        if memorize_mode:
            st.warning("🙈 **暗記モード中**：黄色く隠された部分にカーソルを合わせる（スマホはタップする）と答えが表示されます。")
        if search_query.strip():
            st.info(f"🔍 検索キーワード：「**{search_query.strip()}**」で絞り込み中")

        # 目的と必要物品を縦並びで表示
        st.subheader("🎯 目的")
        st.write(current_proc["purpose"])

        st.subheader("🧰 必要物品")
        st.write("・" + " ・".join(current_proc["items"]))

        st.markdown("---")
        st.subheader("📝 手順と重要ポイント")
        st.caption(
            "※ 左のチェックボックスを入れると、その手順に水色マーカーが引かれます（重要な黄色マーカーはそのまま残ります）。"
        )

        for idx, step_data in enumerate(current_proc["steps"]):
            col_chk, col_body = st.columns([0.05, 0.95])
            with col_chk:
                is_checked = st.checkbox(
                    "マーカー",
                    key=f"{proc_id}_step_{idx}",
                    label_visibility="collapsed",
                )
            with col_body:
                st.markdown(f"**{step_data['step']}**")
                action_html = (
                    f"<span class='user-marker'>{step_data['action']}</span>"
                    if is_checked
                    else step_data["action"]
                )
                st.markdown(action_html, unsafe_allow_html=True)
                st.markdown(
                    f"<div class='point-box'>💡 <strong>根拠・留意点：</strong>{step_data['rationale']}</div>",
                    unsafe_allow_html=True,
                )

# === タブ2：確認回数グラフ ===
with tab_chart:
    st.title("📊 基礎看護技術 確認回数グラフ")
    st.caption("どの技術を何回確認したかを一覧で比較できます。確認回数が0回の技術を優先して復習しましょう。")

    total_procs = len(NURSING_PROCEDURES)
    reviewed_procs = sum(1 for count in st.session_state.review_counts.values() if count > 0)
    unreviewed_count = total_procs - reviewed_procs

    m1, m2 = st.columns(2)
    m1.metric("確認済みの技術", f"{reviewed_procs} / {total_procs} 手技")
    m2.metric("未確認の技術", f"{unreviewed_count} 手技")

    st.markdown("---")

    chart_records = []
    for p in NURSING_PROCEDURES:
        chart_records.append(
            {
                "カテゴリー": p["category"],
                "手技名": p["title"],
                "確認回数": st.session_state.review_counts[p["id"]],
            }
        )
    df_chart = pd.DataFrame(chart_records)

    # 2つのグラフの縦軸（Y軸）位置を完全に揃えるための共通ラベル幅設定
    Y_AXIS_WIDTH = 280

    # 軸のズーム・スクロール変動を無効化した横棒グラフ（手技別）
    st.subheader("📋 手技別の確認回数")
    max_proc_count = max(int(df_chart["確認回数"].max()), 5)
    proc_chart = (
        alt.Chart(df_chart)
        .mark_bar(color="#fbc02d", cornerRadiusEnd=4)
        .encode(
            x=alt.X(
                "確認回数:Q",
                title="確認回数（回）",
                scale=alt.Scale(domain=[0, max_proc_count]),
                axis=alt.Axis(tickMinStep=1, format="d"),
            ),
            y=alt.Y(
                "手技名:N",
                sort=df_chart["手技名"].tolist(),
                title=None,
                axis=alt.Axis(
                    labelLimit=Y_AXIS_WIDTH - 10,
                    minExtent=Y_AXIS_WIDTH,
                    maxExtent=Y_AXIS_WIDTH,
                ),
            ),
            tooltip=["カテゴリー", "手技名", "確認回数"],
        )
        .properties(height=max(420, len(df_chart) * 32))
        .configure_view(strokeWidth=0)
    )
    st.altair_chart(proc_chart, use_container_width=True)

    st.markdown("---")

    # 軸のズーム・スクロール変動を無効化した横棒グラフ（カテゴリー別）
    st.subheader("📂 カテゴリー別の確認回数")
    df_cat = (
        df_chart.groupby("カテゴリー", as_index=False, sort=False)["確認回数"]
        .sum()
    )
    max_cat_count = max(int(df_cat["確認回数"].max()), 5)
    cat_chart = (
        alt.Chart(df_cat)
        .mark_bar(color="#42a5f5", cornerRadiusEnd=4)
        .encode(
            x=alt.X(
                "確認回数:Q",
                title="確認回数（回）",
                scale=alt.Scale(domain=[0, max_cat_count]),
                axis=alt.Axis(tickMinStep=1, format="d"),
            ),
            y=alt.Y(
                "カテゴリー:N",
                sort=df_cat["カテゴリー"].tolist(),
                title=None,
                axis=alt.Axis(
                    labelLimit=Y_AXIS_WIDTH - 10,
                    minExtent=Y_AXIS_WIDTH,
                    maxExtent=Y_AXIS_WIDTH,
                ),
            ),
            tooltip=["カテゴリー", "確認回数"],
        )
        .properties(height=max(260, len(df_cat) * 36))
        .configure_view(strokeWidth=0)
    )
    st.altair_chart(cat_chart, use_container_width=True)

    with st.expander("🔢 数値一覧テーブルを表示"):
        st.dataframe(df_chart, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("※ 本アプリの記載内容は一般的な基礎看護教育の標準手順をもとに作成したサンプルです。実際の臨地実習や臨床現場では、各施設・教育機関の最新プロトコルに従ってください。")

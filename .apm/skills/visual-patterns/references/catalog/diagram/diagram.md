# diagram の分類

diagram に属する趣旨の定義と、候補パターンの決め方。
分類体系の全体、趣旨の定義項目、情報構造や制約の語彙は `../taxonomy.md` を参照。

## 1. 参照元

diagram のパターンは、A Periodic Table of Visualization Methods（Lengler & Eppler, 2007）に挙がる
100 の方法を整理して登録する。

- https://www.visual-literacy.org/periodic_table/periodic_table.html
- 論文: https://www.visual-literacy.org/periodic_table/periodic_table.pdf

周期表は経営向けの「視覚化の方法」を集めたもので、
文書の図だけでなく、思考や対話を支援する手法を含む。
本書の対象（`../taxonomy.md` 1.1）に当たるものだけを登録し、
残りも 4 節の対応表に扱いと理由を残す。

## 2. 周期表の次元と本書の対応

| 周期表の次元 | 本書での扱い |
| --- | --- |
| グループ（データ・情報・概念・戦略・比喩・複合） | 表現形式の判定には使わない。family は `../taxonomy.md` 4.1 の分類原則で決める。情報グループには chart（Treemap）と diagram（ER diagram）が混在し、データグループには table（Table）がある。複合は Composition に相当するが、挙がる方法はいずれも対象外 |
| 周期（複雑さ） | 記法の規則の数で定義されており、本書の complexity（読み手に要求する記法の知識）とは一致しない。参考にとどめる |
| 型（プロセス・構造） | 情報構造（3.2）の目安。プロセスは sequence か向きのある graph、構造は hierarchy か graph に当たることが多い |
| 視点（概観・詳細・両方） | 精度（3.3）の目安。概観は overview、詳細は exact に近い |
| 思考（収束・発散） | 対応しない。本書は読み手への伝達を目的とし、発想の支援は扱わない |

## 3. 採用の基準

`../taxonomy.md` 1.1 の対象（文書内で情報の理解を補助する視覚表現）に当たり、
以下の除外のいずれにも当たらない方法を登録する。

| 扱い | 基準 |
| --- | --- |
| 登録済み | Visual Vocabulary 由来の chart、または既存の diagram として登録済み |
| 既存に含める | 既存のパターンと符号化が同じで、差が外観か内容だけ（`../taxonomy.md` 7章「新規パターン」） |
| 分野固有 | 特定の分野の内容や記法に結びついた枠組み。一般形があるものはそのパターンの利用例とし（既存に含める）、一般形がないものは対象外とする（adr/0004） |
| 思考・対話の手法 | 図は作業の過程で生まれ、文書の図として単独では読めない |
| 対話操作が前提 | 焦点の移動や回転などの操作がなければ読めず、静的な文書に置けない |
| 構成要素 | 単独のパターンではなく、他のパターンの部品 |
| 比喩 | 比喩の形に情報を載せる方法。当てはまる趣旨があるものは候補として登録し、`when` に比喩であることを示す。当てはまる趣旨がないものは対象外（adr/0004） |
| 検討中 | 記法が形式的で、候補にするか検討中（adr/0005） |

登録した 34 件のうち、Table・Timeline・Gantt chart は 4.1 の分類原則により family を table・chart とする。
Organisation chart と Portfolio diagram は、それぞれの一般形である樹形図（`tree-diagram`）と
2軸マトリクス（`quadrant-matrix`）の名前で登録し、組織図とポートフォリオ図はその利用例とする（adr/0004）。

「既存に含める」の利用例は、パターン本文を書く際に「利用例」節へ写す。
比喩として登録した 5 件は、意図しない意味（手順2 の末尾の制約）を読ませやすいため、手順9 の逆読みで確かめる。

## 4. 周期表の方法と本書の対応

型は周期表の記載（プロセス・構造）をそのまま写す。

| 周期表の名称 | グループ | 型 | 扱い | パターン / 理由 |
| --- | --- | --- | --- | --- |
| Continuum | データ | 構造 | 登録 | `continuum` |
| Table | データ | 構造 | 登録 | `data-table` |
| Cartesian coordinates | データ | 構造 | 構成要素 | チャートの座標系そのもの |
| Pie chart | データ | 構造 | 登録済み | `pie-chart` |
| Line chart | データ | 構造 | 登録済み | `line-chart` |
| Bar chart | データ | 構造 | 登録済み | `bar-chart`（縦横は属性。adr/0002） |
| Area chart | データ | 構造 | 登録済み | `area-chart` |
| Histogram | データ | 構造 | 登録済み | `histogram` |
| Scatterplot | データ | 構造 | 登録済み | `scatter-plot` |
| Tukey box plot | データ | 構造 | 登録済み | `box-plot` |
| Spectrogram | データ | 構造 | 分野固有 | 信号の計測表示 |
| Timeline | 情報 | プロセス | 登録 | `timeline`（family は chart） |
| Parallel coordinates | 情報 | 構造 | 登録済み | `parallel-coordinates` |
| Hyperbolic tree | 情報 | 構造 | 対話操作が前提 | 焦点を動かして読む |
| Cycle diagram | 情報 | プロセス | 登録 | `cycle-diagram` |
| Sankey diagram | 情報 | 構造 | 登録済み | `sankey` |
| Venn / Euler diagram | 情報 | 構造 | 登録 | `venn-diagram` |
| Radar chart / cobweb | 情報 | 構造 | 登録済み | `radar-chart` |
| Information lens | 情報 | 構造 | 対話操作が前提 | 行を伸縮して読む（table lens） |
| Entity relationship diagram | 情報 | 構造 | 登録 | `er-diagram` |
| Petri net | 情報 | プロセス | 検討中 | 状態変化・並列を定義する際の候補（adr/0005） |
| Data map | 情報 | 構造 | 登録済み | `choropleth-map` |
| Clustering | 情報 | 構造 | 登録 | `cluster-diagram` |
| Cone tree | 情報 | 構造 | 対話操作が前提 | 3D を回転して読む |
| Treemap | 情報 | 構造 | 登録済み | `treemap` |
| Flow chart | 情報 | プロセス | 登録済み | `flowchart` |
| Semantic network | 情報 | 構造 | 既存に含める | `concept-map`。ノードとラベル付きの辺という符号化が同じ |
| Data flow diagram | 情報 | プロセス | 登録 | `data-flow-diagram` |
| System dynamics / simulation | 情報 | プロセス | 登録 | `stock-flow-diagram` |
| Concept skeleton | 概念 | 構造 | 思考・対話の手法 | 概念整理の雛形 |
| Meeting trace | 概念 | プロセス | 思考・対話の手法 | 会議の進行の記録 |
| Flight plan | 概念 | プロセス | 思考・対話の手法 | プロジェクトの進め方の雛形 |
| Concept fan | 概念 | 構造 | 思考・対話の手法 | 発想法 |
| Mindmap | 概念 | 構造 | 登録 | `mind-map` |
| Square of oppositions | 概念 | 構造 | 分野固有 | 論理学の命題関係 |
| Concentric circles | 概念 | 構造 | 登録 | `concentric-circles` |
| Argument slide | 概念 | 構造 | 既存に含める | `toulmin-map`。主張・根拠・帰結の提示形式が違うだけ |
| Communication diagram | 概念 | プロセス | 登録 | `communication-diagram` |
| Gantt chart | 概念 | プロセス | 登録 | `gantt-chart`（family は chart） |
| Perspectives diagram | 概念 | 構造 | 思考・対話の手法 | 経験を整理する雛形 |
| Dilemma diagram | 概念 | 構造 | 思考・対話の手法 | 判断の帰結を検討する雛形 |
| Layer chart | 概念 | 構造 | 登録 | `layer-diagram` |
| Minto pyramid technique | 概念 | 構造 | 登録 | `minto-pyramid` |
| Cause effect chains | 概念 | 構造 | 登録 | `cause-effect-chain` |
| Toulmin map | 概念 | 構造 | 登録 | `toulmin-map` |
| Decision tree | 概念 | プロセス | 登録済み | `decision-tree` |
| Critical path method | 概念 | プロセス | 既存に含める | `pert-chart`。同じ活動ネットワーク上で最長経路を求める手法 |
| Evocative knowledge map | 概念 | 構造 | 思考・対話の手法 | 知識の所在を探す雛形 |
| Concept map | 概念 | 構造 | 登録 | `concept-map` |
| Soft system modeling | 概念 | プロセス | 思考・対話の手法 | 問題状況を絵にする手法 |
| Synergy map | 概念 | 構造 | 思考・対話の手法 | 目標間の相互作用を検討する雛形 |
| Force field diagram | 概念 | 構造 | 登録 | `force-field-diagram` |
| IBIS argumentation map | 概念 | 構造 | 登録 | `ibis-map` |
| Process event chains | 概念 | プロセス | 検討中 | 記法が特定の手法（ARIS）に固有。分岐の候補にするか検討中（adr/0005） |
| PERT chart | 概念 | プロセス | 登録 | `pert-chart` |
| Swim lane diagram | 概念 | プロセス | 登録 | `swim-lane-diagram` |
| Vee diagram | 概念 | 構造 | 分野固有 | V 字モデル（開発工程と検証の対応） |
| Supply demand curve | 戦略 | 構造 | 分野固有 | 経済学の需給モデル |
| Performance charting | 戦略 | 構造 | 分野固有 | 要求と実績の対比の雛形 |
| Strategy map | 戦略 | 構造 | 既存に含める | `cause-effect-chain` の利用例（バランスト・スコアカード） |
| Organisation chart | 戦略 | 構造 | 登録 | `tree-diagram`（一般名で登録。組織図は利用例） |
| House of quality | 戦略 | 構造 | 分野固有 | 品質機能展開の複合マトリクス |
| Feedback diagram | 戦略 | 構造 | 登録 | `feedback-diagram` |
| Failure tree | 戦略 | 構造 | 登録 | `fault-tree` |
| Magic quadrant | 戦略 | 構造 | 既存に含める | `quadrant-matrix` の利用例 |
| Stakeholder rating map | 戦略 | 構造 | 既存に含める | `quadrant-matrix` の利用例 |
| Porter's five forces | 戦略 | 構造 | 分野固有 | 五つの競争要因の枠組み |
| S-cycle | 戦略 | プロセス | 分野固有 | 技術普及の概念曲線 |
| Stakeholder map | 戦略 | 構造 | 既存に含める | `cluster-diagram` の利用例（中心の対象に対する関係者のグループ分け） |
| Life cycle diagram | 戦略 | プロセス | 分野固有 | 製品ライフサイクルの概念曲線 |
| Technology roadmap | 戦略 | プロセス | 登録 | `technology-roadmap` |
| Edgeworth box | 戦略 | 構造 | 分野固有 | 経済学の交換モデル |
| Portfolio diagram | 戦略 | 構造 | 登録 | `quadrant-matrix`（一般名で登録。ポートフォリオ図は利用例） |
| Strategic game board | 戦略 | 構造 | 分野固有 | 競争戦略の三軸の枠組み |
| Mintzberg's organigraph | 戦略 | 構造 | 分野固有 | 組織形態の図式の枠組み |
| Zwicky's morphological box | 戦略 | 構造 | 思考・対話の手法 | 発想法（形態分析） |
| Affinity diagram | 戦略 | 構造 | 登録 | `affinity-diagram` |
| Decision discovery diagram | 戦略 | プロセス | 思考・対話の手法 | 意思決定の経緯を振り返る雛形 |
| BCG matrix | 戦略 | 構造 | 既存に含める | `quadrant-matrix` の利用例 |
| Strategy canvas | 戦略 | 構造 | 分野固有 | 競争要因ごとの価値曲線 |
| Value chain | 戦略 | プロセス | 分野固有 | 主活動と支援活動の枠組み |
| Hype cycle | 戦略 | プロセス | 分野固有 | 技術の期待度の概念曲線 |
| Ishikawa diagram | 戦略 | 構造 | 登録 | `ishikawa-diagram` |
| TAPS | 戦略 | 構造 | 思考・対話の手法 | 施策を選ぶ手法 |
| Spray diagram | 戦略 | 構造 | 既存に含める | `mind-map`。放射状の階層という符号化が同じ |
| Metro map | 比喩 | プロセス | 登録 | `metro-map`（比喩。工程の候補） |
| Temple | 比喩 | 構造 | 登録 | `temple`（比喩。層の候補） |
| Story template | 比喩 | 構造 | 比喩（対象外） | 当てはまる趣旨がない（物語の構成） |
| Tree | 比喩 | 構造 | 登録 | `tree-metaphor`（比喩。親子関係の候補） |
| Bridge | 比喩 | 構造 | 比喩（対象外） | 当てはまる趣旨がない（交渉の進め方） |
| Funnel | 比喩 | プロセス | 登録 | `funnel`（比喩。流量の候補） |
| Parameter ruler | 比喩 | 構造 | 比喩（対象外） | 当てはまる趣旨がない（評価の目盛り） |
| Iceberg diagram | 比喩 | 構造 | 登録 | `iceberg`（比喩。層の候補） |
| Heaven 'n' hell chart | 比喩 | 構造 | 比喩（対象外） | 当てはまる趣旨がない（振り返り） |
| Graphic facilitation | 複合 | 構造 | 思考・対話の手法 | 対話の場で描く |
| Cartoon | 複合 | 構造 | 思考・対話の手法 | 物語として描く |
| Rich picture | 複合 | 構造 | 思考・対話の手法 | 問題状況を絵にする |
| Knowledge map | 複合 | 構造 | 思考・対話の手法 | 知識の所在を地図の比喩で描く |
| Learning map | 複合 | プロセス | 思考・対話の手法 | 学習内容を絵にする |
| Infomural | 複合 | 構造 | 思考・対話の手法 | 壁面大の全体像 |

## 5. 候補の決め方

周期表は候補の優先順を示さない。
各趣旨の第一候補は、最も一般的で読み手が記法を知っている可能性が高いものとし、
残りは読み手の認知コストが低い順に並べて（`../taxonomy.md` 6.4）、切り替える条件（`when`）を付ける。

候補と切替条件は `../index.yaml` に定義する。

Visual Vocabulary の Venn・Network は diagram に属するため、
所属・関連の候補としてここで登録する（`../chart/chart.md` 3）。

## 6. 趣旨の定義

定義項目（問い・前提・境界）は `../taxonomy.md` 3.1 に従う。
境界で参照する趣旨のうち、diagram に属さないものは、他の表現形式の分類文書（`../chart/chart.md`、`../table/table.md`）で定義する。

### 比較

#### 位置づけ (`positioning`)

対象を評価の軸の上に置き、相対的な位置を示す。

- 問い: それは軸のどこに位置するか、どの象限に入るか
- 前提: `items: categorical + ordinal`（軸は一つか二つ。位置は測定値ではなく評価で決める）
- 境界:
  - 軸が測定値で、二つの量の連動が主題の場合は「相関」を使用する
  - 観点が三つ以上ある場合は「属性比較」を使用する
  - 地理的な位置の場合は「地理」を使用する

### 変化

#### 経緯 (`chronology`)

出来事がいつ、どの順で起きたかを示す。

- 問い: 何がいつ、どの順で起きたか
- 前提: `items: temporal + categorical`（出来事と時点。量はない）
- 境界:
  - 量の推移が主題の場合は「時系列変化」を使用する
  - 期間・並行・依存を伴う計画の場合は「工程」を使用する
  - 主体の間のやり取りの順が主題の場合は「実行順」を使用する

### 関係

#### 関連 (`relationship`)

何が何と、どのような関係で結ばれているかを示す。

- 問い: 何が何と、どう関係しているか
- 前提: `graph: categorical`（辺が関係の種類を持つ。向きは問わない）
- 境界:
  - 関係が原因から結果への向きを持つ場合は「因果」を使用する
  - 二つの量の連動が主題の場合は「相関」を使用する
  - 関係が親子だけの場合は「親子関係」を使用する
  - 辺に量があり、移動が主題の場合は「流量」を使用する

#### 因果 (`causation`)

何が原因で何が起きるかを示す。

- 問い: 何が原因で何が起きるか
- 前提: `graph`（向きがあり、辺が原因から結果を表す。ループを含んでよい）
- 境界:
  - 連動を示すにとどまり、向きを主張しない場合は「相関」を使用する
  - 条件によって処理の流れが分かれることが主題の場合は「分岐」を使用する
  - 繰り返す段階の順序が主題の場合は「循環」を使用する
  - 向きのない関係の場合は「関連」を使用する

#### 依存 (`dependency`)

何が何を必要とし、変更がどこへ及ぶかを示す。

- 問い: 何が何を必要とし、変更はどこに影響するか
- 前提: `graph`（向きがあり、辺が必要とする側から必要とされる側へ向かう。データの受け渡しを含む）。
  候補のデータフロー図は辺をデータの移動の向き（送る側から受ける側）で描くので、依存の辺とは向きが逆になる。
  作図時に向きを変える（`data-flow-diagram.md`「入力の構造」）。データの移動を伴わない依存には候補がなく、文章か表で示す（`../taxonomy.md` 1.4）
- 境界:
  - 作業の時期と並行が主題の場合は「工程」を使用する
  - 向きのない関係の場合は「関連」を使用する
  - 原因と結果の連鎖が主題の場合は「因果」を使用する
  - 辺に量があり、移動した量が主題の場合は「流量」を使用する

#### 対立 (`opposing-forces`)

変化を推進する要因と妨げる要因を対置して示す。

- 問い: 何が推進し、何が妨げるか
- 前提: `items: categorical`（要因が推進か抑制かの区分を持つ。強さを示すなら ordinal を加える）
- 境界:
  - 原因から結果への連鎖が主題の場合は「因果」を使用する
  - 基準からの正負の量を比べる場合は「偏差」を使用する
  - 複数の対象を観点ごとに見比べる場合は「属性比較」を使用する

### 構造

#### 親子関係 (`parent-child`)

何が何の下位にあるかを示す。

- 問い: 何が何の下位にあり、全体はどう枝分かれするか
- 前提: `hierarchy: categorical`
- 境界:
  - 各部分が全体に占める割合も読ませる場合は「構成」を使用する
  - 条件を辿って結論に着く場合は「条件判定」を使用する
  - 主張と根拠の階層の場合は「論証」を使用する
  - 項目が複数のグループに属しうる場合は「所属」を使用する

#### 所属 (`membership`)

何がどのグループに属するかを示す。

- 問い: 何がどのグループに属し、グループは重なるか
- 前提: `items: categorical`（グループを表す属性。項目は複数のグループに属してよい）
- 境界:
  - グループが入れ子で、項目が一つの親にだけ属す場合は「親子関係」を使用する
  - 入れ子の層そのものが主題の場合は「層」を使用する
  - 項目同士の個別の関係を示す場合は「関連」を使用する

#### 層 (`layering`)

何が何の上に成り立つか、何が内側にあるかを示す。

- 問い: 何が何の上に成り立ち、何が内側（下側）にあるか
- 前提: `sequence: categorical`（層の順序。入れ子でもよい）
- 境界:
  - 各層が全体に占める割合が主題の場合は「構成」を使用する
  - 層の中が枝分かれする場合は「親子関係」を使用する
  - 重なりうるグループへの所属が主題の場合は「所属」を使用する

#### 論証 (`argumentation`)

結論が何に支えられているかを示す。

- 問い: 結論は何に支えられ、何が反論か
- 前提: `hierarchy: categorical`（主張が親、根拠が子。反論を含める場合は graph）
- 境界:
  - 原因と結果の関係の場合は「因果」を使用する
  - 条件から結論が一つに決まる場合は「条件判定」を使用する
  - 主張を伴わない分解の場合は「親子関係」を使用する

### プロセス

#### 実行順 (`step-order`)

何がどの順に起こるかを示す。

- 問い: 何がどの順に起こるか、誰が誰に何を渡すか
- 前提: `sequence: categorical`（categorical はやり取りの主体。二つ以上）
- 境界:
  - 主体が一つで分岐もない場合は図表にせず、番号付きリストで書く（手順2）
  - 条件による流れの分かれ方が主目的の場合は「分岐」を使用する

#### 分岐 (`branching`)

処理の流れが条件によってどう分かれるかを示す。

- 問い: どの条件で、流れがどう分かれるか
- 前提: `graph`（向きがあり、分岐を一つ以上含む）
- 境界:
  - 分岐がない場合は「実行順」を使用する
  - 途中に作業を挟まず、条件だけを辿って結論に着く場合は「条件判定」を使用する

#### 工程 (`schedule`)

作業をいつからいつまで行い、何が並行し、何が何を待つかを示す。

- 問い: 何をいつからいつまで行い、何が並行し、何が何を待つか
- 前提: `items: categorical + temporal`（作業と期間。作業間に依存があれば graph）
- 境界:
  - 期間を持たない出来事の列の場合は「経緯」を使用する
  - 作業の中の条件による分かれ方が主題の場合は「分岐」を使用する
  - 主体が一つで、並行も依存もない場合は図表にせず、番号付きリストで書く（手順2）

#### 循環 (`cycle`)

段階が繰り返し、どこへ戻るかを示す。

- 問い: どの段階を経て、どこへ戻るか
- 前提: `sequence: categorical`（末尾が先頭へ戻る）
- 境界:
  - 戻りのない順序の場合は「実行順」を使用する
  - 段階の間の因果が主題の場合は「因果」を使用する

### 参照

#### 条件判定 (`conditional-outcome`)

条件を当てはめると結論が一つに決まることを示す。

- 問い: この条件に当てはまる場合、結論はどれか
- 前提: `hierarchy: categorical`（条件が親、選択肢が枝、結論が葉）
- 境界:
  - 結論が一つに決まらず、判断を読み手に委ねる場合は「属性比較」を使用する
  - 条件の間に作業が挟まる場合は「分岐」を使用する

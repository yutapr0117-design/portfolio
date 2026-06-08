/**
 * ════════════════════════════════════════════════════════════════════════════
 * js/quiz/aws-quiz-data.js — AWS 問題集データ（単一データセット・静的）
 * ════════════════════════════════════════════════════════════════════════════
 *
 * @fileoverview
 * v80+ Stage 3-b（ドメイン別細分化）。Stage 3 で main.js から 1 ファイルへまとめて抽出した
 * 静的クイズデータ `js/quiz-data.js`（4 データセット同居・約 1,406 行）を、保守性向上のため
 * **ドメイン別の 4 つの葉モジュールへさらに分割**したうちの 1 つ。本ファイルは
 * `awsQuizData` ただ 1 つを export する。
 *
 * ── 非破壊性の保証（最重要）─────────────────────────────────────────────────
 * 本ファイルの `export const awsQuizData = {...};` ブロックは、分割前の
 * `js/quiz-data.js` の該当行範囲（39–822 行）を **1 バイトも変えずに** 切り出した
 * ものである（プログラムによる行 slice。手入力転記を一切行わないことで「大きな塊を移す際の
 * 一部取りこぼし／改変」事故を物理的に排除）。設問本文・意図・選択肢はプロダクトの中身で
 * あり、要約・中立化・省略は禁止。
 *
 * ── 葉モジュール契約（機械強制）───────────────────────────────────────────
 * 本ファイルは依存ゼロの葉モジュール（import を一切持たない）であり、関数も副作用も持たない
 * 純データである。出力も振る舞いも無いため、読み込み順序・DOM・クロージャ状態に非依存——
 * どこへ移しても挙動は変わらない。`main.js` はこの単一 export を直接 import し、
 * `Check 47`（import/export bijection と葉モジュール性）が main.js の import と本ファイルの
 * export の一致を BLOCKING で機械強制する。lint 被覆は `Check 46`（root ∪ js/）が、ディスク上の
 * js/ 配下（再帰）の .js ファイルを `package.json` の `lint`/`lint:js` 両スクリプトに含めることを BLOCKING で強制する。
 *
 * ── 読み込み機構 ───────────────────────────────────────────────────────────
 * `index.html` が `main.js` を `<script type="module">` で読み込み、`main.js` が本モジュールを
 * `import { awsQuizData } from './js/quiz/aws-quiz-data.js';` で取り込む。CSP `script-src 'self'` の
 * ため同一オリジン取得に追加設定は不要。
 * ════════════════════════════════════════════════════════════════════════════
 */

'use strict';

export const awsQuizData = {
            "1. コンピュート & インスタンス (EC2, EBS)": [
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS)",
                    "id": "Q1",
                    "title": "Q1. ステータスチェックの厳密な切り分け",
                    "content": [
                        "状況: EC2が応答しない。「システムステータスチェック」が失敗している。",
                        "問: 再起動（Reboot）ではなく「停止・開始（Stop/Start）」を選択すべき技術的理由は何か？この操作によってAWS内部で何が行われるか？"
                    ]
                },
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS) - 上級編",
                    "id": "Q1",
                    "title": "Q1. インスタンス障害の厳密な切り分けとリカバリ・自動化戦略",
                    "content": [
                        "本番稼働中のEC2インスタンス（Linux）へのSSH接続がタイムアウトし、サービス応答も途絶えた。CloudWatchを確認すると「システムステータスチェック（System Status Check）」が失敗している。一方で「インスタンスステータスチェック」は成功しているように見える。このインスタンスはASG（Auto Scaling Group）管理下にあるが、なぜか自動復旧していない。",
                        "Challenge",
                        "「システムステータスチェック」と「インスタンスステータスチェック」の失敗が示す物理的・論理的な責任境界を、ハイパーバイザーとOSのレイヤーから厳密に定義せよ。",
                        "この状況で、オペレーターが手動で Reboot を実行しても問題が解決しない可能性が高い技術的理由と、Stop/Start が物理ホストレベルで何を引き起こすか（Migrationメカニズム）を解説せよ。",
                        "ASGのヘルスチェックタイプが「EC2」であるにもかかわらず、システムステータスチェック失敗時に即座に置換されないケースがある。ASGがEC2の不調を検知してインスタンスを置換するための正確な条件と、「EC2 Auto Recovery」との機能的な違いを述べよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "境界点:",
                        "システムステータスチェック: AWS側の責任範囲。物理ホストの電源、ネットワーク接続、物理ディスク、またはハイパーバイザー（Nitro System等）自体の障害を示す。ユーザーの操作では修復不可能。",
                        "インスタンスステータスチェック: ユーザー側の責任範囲。ゲストOSのカーネルパニック、ファイルシステム破損、ネットワーク設定ミス（iptables/NIC設定）、メモリ枯渇によるプロセスハングなどが原因。",
                        "Reboot vs Stop/Start:",
                        "Reboot は同一物理ホスト上でのOS再起動に過ぎないため、物理ホスト自体（システムステータス）に障害がある場合は復旧しない。",
                        "Stop はインスタンスと物理ホストの紐付けを解除し、Start は健全な別の物理ホストへインスタンスを新規配置（Migration）する操作であるため、物理障害からの確実な回避策となる。",
                        "注意: インスタンスストア（Ephemeral Storage）のデータはStopにより完全に消失する。",
                        "ASG vs Auto Recovery:",
                        "ASGの「EC2」ヘルスチェックは、ステータスチェック失敗を検知してインスタンスをTerminate & Replace（削除して新規作成）する。ステートフルなデータは消える。",
                        "EC2 Auto Recoveryは、インスタンスをTerminateせず、同じインスタンスID、同じEBSボリューム、同じEIPを保持したままStop/Start相当の復旧（物理ホスト移動）を自動で行う。",
                        "現場の視点: 単なるWebサーバーならASGの置換で良いが、固定IPや特定EBSが必要な管理サーバー等はEC2 Auto Recoveryを設定すべき。"
                    ]
                },
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS)",
                    "id": "Q2",
                    "title": "Q2. インスタンスステータスチェック失敗時のレスキュー",
                    "content": [
                        "状況: 「インスタンスステータスチェック」が失敗し、SSHも繋がらない。重要データがありTerminateできない。",
                        "問: ログ調査とファイルシステム修復のために行う「レスキューインスタンス」の手順とは？"
                    ]
                },
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS) - 上級編",
                    "id": "Q2",
                    "title": "Q2. EBS (gp2/gp3/io2) のパフォーマンス仕様とスループットの罠",
                    "content": [
                        "レガシーなDBサーバーで gp2 ボリューム（500GB）を使用している。IOPS上限（1,500 IOPS）には達していないが、バッチ処理中にディスクレイテンシが悪化し、CloudWatchの BurstBalance が0%に張り付いている。コスト削減と性能安定のため gp3 への移行を計画したが、移行後にIOPSは足りているはずなのに、逆に処理時間が2倍に延びる障害が発生した。",
                        "Challenge:",
                        "gp2 における「クレジットバケツモデル」の計算式（ベースラインIOPSと蓄積レート）に基づき、500GBボリュームがバースト枯渇を起こすメカニズムを数値で証明せよ。",
                        "gp3 移行時に多くのエンジニアが見落とす「スループット（MiB/s）」のデフォルト制限値と、それがDBのシーケンシャルリード/ライトに与える影響を説明せよ。",
                        "ミッションクリティカルなDBにおいて、gp3 ではなくあえて io2 Block Express を選択すべき技術的条件（レイテンシ、耐久性、マルチアタッチ）を挙げよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "gp2の枯渇:",
                        "ベースラインは 3 IOPS/GB。500GBの場合、500 * 3 = 1,500 IOPS がベースライン。",
                        "3,000 IOPSまでバースト可能だが、ベースラインを超過中はクレジットを消費する。クレジットが枯渇すると、強制的に1,500 IOPSに制限（スロットリング）される。",
                        "gp3の罠 (Throughput):",
                        "gp3 はベースライン3,000 IOPSを保証するが、スループットのデフォルトは 125 MiB/s である。",
                        "一方、gp2 (500GB) のスループット上限はバースト時 250 MiB/s まで出る仕様になっている（容量依存）。",
                        "失敗原因: 移行時にスループット設定をデフォルト（125 MiB/s）のままにしたため、帯域幅が半分になり、大量のデータを読み書きするバッチ処理が遅延した。gp3では明示的にスループットを追加購入する必要がある。",
                        "io2 Block Expressの出番:",
                        "サブミリ秒の低レイテンシが必要な場合。",
                        "99.999% (ファイブナイン) の耐久性が必要な場合（gp3は99.8-99.9%）。",
                        "Multi-Attach（複数のEC2から同時に書き込み可能なクラスタ構成）が必要な場合。"
                    ]
                },
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS)",
                    "id": "Q3",
                    "title": "Q3. インスタンスストアの揮発性",
                    "content": [
                        "状況: インスタンスストア（Ephemeral Storage）を持つインスタンスタイプ（i3など）をStop/Startした。",
                        "問: インスタンスストア内のデータはどうなるか？また、Rebootの場合はどうなるか？",
                        "リソースとパフォーマンス"
                    ]
                },
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS) - 上級編",
                    "id": "Q3",
                    "title": "Q3. インスタンス起動時のデバッグとUser Data",
                    "content": [
                        "Auto Scaling Groupで起動したインスタンスが、アプリの起動スクリプト（User Data）のエラーにより Unhealthy と判定され、ログを確認する前にTerminateされてしまう現象がループしている。User DataはBase64エンコードされており、手動デコードしても構文エラーは見当たらない。",
                        "Challenge:",
                        "起動失敗したインスタンスをTerminateさせずに一時停止（Pending:Wait / Terminating:Wait）させ、デバッグを行うためのASG機能とその具体的な設定フック名を答えよ。",
                        "Linuxにおける cloud-init の実行フェーズ（init、 config、 final）において、User Data（シェルスクリプト）はどの段階で実行されるか？ また、標準出力・エラー出力が記録される完全なログパスを示せ。",
                        "User Dataが正しく記述されているにもかかわらず、スクリプトが途中終了したり実行されない場合によくある、「改行コード」や「シェバン（#!）」にまつわるトラブル原因を挙げよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "Lifecycle Hooks:",
                        "ASGの Lifecycle Hook を設定する。",
                        "起動時デバッグなら autoscaling:EC2_INSTANCE_LAUNCHING フックで、遷移を Pending:Wait 状態で止める。これによりSSH/SSMでログインして調査が可能になる。",
                        "cloud-initの動作:",
                        "User Data（シェルスクリプト）は通常 final フェーズ（起動処理の最後）で実行される。",
                        "ログファイル: /var/log/cloud-init-output.log（スクリプトの標準出力/エラー出力はここ）。構造化ログは /var/log/cloud-init.log。",
                        "現場の罠:",
                        "Windowsで作成したファイルの改行コードが CRLF になっていると、Linuxのbashが解釈できずエラーになる（LF必須）。",
                        "#!/bin/bash のシェバンがないと、cloud-initがスクリプトとして認識しない場合がある。",
                        "Tech Lead's Tip: 本番でASGを止めるより、同じAMIとUser Dataを使って手動で単発インスタンスを起動し、再現確認するほうが安全かつ迅速な場合が多い。"
                    ]
                },
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS)",
                    "id": "Q4",
                    "title": "Q4. T系インスタンスとCPUクレジット",
                    "content": [
                        "状況: T3インスタンスのCPU使用率が20%で張り付き、極端に遅い。",
                        "問: 確認すべきメトリクスはCPUCreditBalanceだが、これを即座に解決するために有効にするモードは？また、そのコストへの影響は？"
                    ]
                },
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS)",
                    "id": "Q5",
                    "title": "Q5. EBSの初期化（ハイドレーション）",
                    "content": [
                        "状況: S3のスナップショットから復元した大容量EBSボリュームが、使用開始直後に激しいレイテンシを示す。",
                        "問: S3からの遅延読み込み（Lazy Loading）によるパフォーマンス低下を防ぐために、使用前に実行すべき操作は？"
                    ]
                },
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS)",
                    "id": "Q6",
                    "title": "Q6. EBSバーストバランス枯渇",
                    "content": [
                        "状況: gp2ボリュームでIOPS制限には達していないが、I/O待ちが増加している。",
                        "問: gp2特有のBurstBalanceメトリクスとは何か？これが枯渇した時の挙動と、gp3への移行メリットは？"
                    ]
                },
                {
                    "section": "1. コンピュート & インスタンス (EC2, EBS)",
                    "id": "Q7",
                    "title": "Q7. OSレベルの制限（No space left on device）",
                    "content": [
                        "状況: ディスク容量不足のエラーが出るが、df -hで見ると容量は余っている。",
                        "問: 容量（ブロック）以外に枯渇している可能性があるファイルシステムのリソースは？確認コマンドは？",
                        "焦点: パケットの消失、非対称ルーティング、DNSの挙動。",
                        "接続性とファイアウォール"
                    ]
                }
            ],
            "2. ネットワーキング(VPC, ELB, DX, DNS)": [
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS) - 上級編",
                    "id": "Q4",
                    "title": "Q4. Security Group vs NACL: ステート管理と戻り通信の落とし穴",
                    "content": [
                        "特定の攻撃的なIPアドレス群からのアクセスをVPCレベルで遮断するため、ネットワークACL（NACL）でInbound DENYルールを設定した。しかし、設定直後から、そのサブネット内のサーバーが外部のリポジトリ（yum/apt）に接続できなくなり、サーバー監視のエージェントもタイムアウトし始めた。SG（セキュリティグループ）の設定は変更していない。",
                        "Challenge:",
                        "SGが「ステートフル」、NACLが「ステートレス」であることを踏まえ、NACLでのInbound遮断が、なぜ無関係なOutbound通信（外部へのリクエスト）の応答パケットに影響を与えるのか、エフェメラルポート（Ephemeral Ports）の挙動を用いて解説せよ。",
                        "サーバーから外部へ通信する場合、NACLのInbound/Outboundルールに最低限どのような許可設定が必要か？ TCPハンドシェイクの往復（SYN -> SYN/ACK -> ACK）に基づいて説明せよ。",
                        "Kubernetes (EKS) 環境において、Pod単位でSGを割り当てる機能（Security Groups for Pods）を使用する場合、ノードレベルのNACL設定との競合や制約について考慮すべき点は何か。",
                        "Core Knowledge & Tech Lead's View:",
                        "戻り通信の死:",
                        "NACLはステートレスなので、「行き」を許可しても「帰り」は自動許可されない。",
                        "サーバーが外部（yumリポジトリ等）へリクエストを送る際、送信元ポートとして エフェメラルポート（1024-65535等） を使用する。",
                        "外部からの応答（SYN/ACK）は、このエフェメラルポート宛てに戻ってくる。",
                        "もしNACLのInboundルールで、特定の攻撃IPを拒否するルールを追加した際、誤ってデフォルトの「Allow ALL」より優先順位が高い位置で広い範囲を拒否していたり、あるいは戻りのエフェメラルポート範囲を明示的に許可していなければ、正規の戻りパケットがドロップされる。",
                        "TCPハンドシェイク:",
                        "Outbound: Server -> External (Dst: 443, Src: 32768) [SYN] -> NACL Outbound許可が必要",
                        "Inbound: External -> Server (Dst: 32768, Src: 443) [SYN/ACK] -> NACL Inboundでポート1024-65535の許可が必要",
                        "EKSのSG:",
                        "Security Groups for Podsを使っても、通信は依然としてサブネットのNACLを通過する。NACLが厳しすぎるとPod通信も阻害される。",
                        "Tech Lead's View: NACLは「特定の攻撃IPを緊急ブロックする」等の用途に限定し、基本はAllow ALLで運用すべき。複雑なNACLはデバッグ不可能な障害を生む。"
                    ]
                },
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS) - 上級編",
                    "id": "Q5",
                    "title": "Q5. DNS at Scale: VPC Resolverの制限とハイブリッドDNS",
                    "content": [
                        "マイクロサービスアーキテクチャを採用し、サービス間通信にDNSベースのサービスディスカバリを使用している。負荷テストを実施したところ、間欠的に名前解決エラー（NameResolutionError）が発生し始めた。また、オンプレミスとDirect Connectで接続された環境で、オンプレ側のDNSサーバーにあるドメインがVPCから引けない問題も発生している。",
                        "Challenge:",
                        "VPC内部DNSリゾルバ（169.254.169.253）に存在する ハードリミット（PPS制限） の具体的な数値と、それがネットワークインターフェース（ENI）単位であることを踏まえた対策（NodeLocal DNSCacheなど）を述べよ。",
                        "Route 53 Resolverの Outbound Endpoint と Forwarding Rule を用いて、VPCからオンプレミスのDNSを解決するアーキテクチャを説明せよ。逆に、オンプレからVPC内のPrivate Hosted Zoneを解決するには何が必要か？",
                        "DNSラウンドロビンによるロードバランシングの限界（クライアントサイドのキャッシュ挙動やスティッキー性）と、それを解決するための最新のサービスディスカバリ手法（AWS Cloud Map、 Envoy等）について論ぜよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "PPS制限:",
                        "VPC DNSへのクエリは 1024 パケット/秒 (PPS) / ENI というハードリミットがある。",
                        "マイクロサービスで短命な接続を大量に繰り返すとこれに抵触する。",
                        "対策: Kubernetesなら NodeLocal DNSCache を導入し、各ノード上でDNSキャッシュを行うことでVPCリゾルバへの問い合わせを減らす。アプリ側でもDNS TTLを適切に扱う。",
                        "ハイブリッドDNS:",
                        "VPC -> On-Prem: Route 53 Resolver Outbound Endpoint を作成し、転送ルール（Forwarding Rule）で「example.corp」等のクエリをオンプレDNSサーバーIPへ転送する。",
                        "On-Prem -> VPC: Route 53 Resolver Inbound Endpoint を作成し、オンプレDNS側で条件付きフォワーダー（Conditional Forwarder）を設定して、VPC内のドメインクエリをInbound EndpointのIPへ飛ばす。",
                        "DNSラウンドロビンの限界:",
                        "Java等のクライアントはDNS解決結果を永続的にキャッシュする傾向があり（TTL無視）、特定のIPに負荷が偏る。",
                        "モダンな対策: Service Mesh (Envoy/App Mesh) や AWS Cloud Map を使い、DNSに依存しないAPIベースのディスカバリや、クライアントサイドロードバランシングを行う。"
                    ]
                },
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS) - 上級編",
                    "id": "Q6",
                    "title": "Q6. Transit Gateway (TGW) の非対称ルーティングとAppliance Mode",
                    "content": [
                        "TGWを中心としたハブ＆スポーク構成で、セキュリティVPC（Inspection VPC）にファイアウォールアプライアンスを配置し、全通信を検査している。しかし、特定のAZ（アベイラビリティゾーン）間の通信だけがファイアウォールで「TCP State Violation」としてドロップされる現象が発生した。",
                        "Challenge:",
                        "TGWがパケット転送時にAZを選択するアルゴリズムと、ステートフルなファイアウォールにおいて非対称ルーティング（Asymmetric Routing）が致命的になる理由を、「行き」と「帰り」の経路差分を用いて説明せよ。",
                        "この問題を解決するためにTGWアタッチメントで有効化すべき 「Appliance Mode」 の技術的な挙動（ハッシュロジックによるフロー固定）を解説せよ。",
                        "TGWのルートテーブルにおける「Blackhole」ルートの活用例をセキュリティの観点から挙げよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "非対称ルーティングの発生:",
                        "TGWはデフォルトでは、パケットの宛先等に基づき最適と判断したAZへ転送するが、往路と復路で同じAZのアタッチメント（ENI）を使う保証がない。",
                        "行き：VPC-A(AZ-a) -> TGW -> Firewall(AZ-a)",
                        "帰り：Firewall(AZ-b) -> TGW -> VPC-A(AZ-a)",
                        "ファイアウォールはAZ間でセッション情報を共有していない場合が多く（あるいは同期ラグがある）、片方向のパケットしか見ていないFWは「不正な通信」としてパケットを破棄する。",
                        "Appliance Mode:",
                        "これを有効にすると、TGWは送信元/宛先IPのハッシュ値を用いて、そのトラフィックフローを常に同じAZのアタッチメントに転送するよう固定する。これにより、行きと帰りで同じFWアプライアンスを経由することが保証される。",
                        "注意: マネジメントコンソールから設定が見えにくい場合があり、CLI/IaCでの明示的な設定が必要。",
                        "Blackholeルート:",
                        "既知の不正なCIDRや、アクセスさせたくないVPC間の通信をTGWレベルで破棄するために使用する。コストのかかるFWでのDropよりも前段で処理できる。"
                    ]
                },
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS)",
                    "id": "Q8",
                    "title": "Q8. NACLのステートレス性",
                    "content": [
                        "状況: セキュリティグループは正しいのにSSHが繋がらない。ネットワークACL（NACL）でインバウンド22を許可している。",
                        "問: NACLが「ステートレス」であることに起因する、戻りパケットのための設定漏れは？"
                    ]
                },
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS)",
                    "id": "Q9",
                    "title": "Q9. ELB 502 vs 504",
                    "content": [
                        "状況: ALBでエラーが発生。",
                        "ケースA: 504 Gateway Timeout",
                        "ケースB: 502 Bad Gateway",
                        "問: それぞれのエラーの原因の違いは？特に502エラーにおいて、「Webサーバー側のKeep-Alive設定」と「ALBのアイドルタイムアウト」の間にどのような不整合があると発生するか？"
                    ]
                },
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS)",
                    "id": "Q10",
                    "title": "Q10. Transit Gatewayと非対称ルーティング",
                    "content": [
                        "状況: TGW経由でファイアウォールアプライアンスを通る通信がドロップされる。行きと帰りの経路が異なるAZを通っている。",
                        "問: ステートフルなファイアウォールがパケットを破棄するのを防ぐために、TGWアタッチメントで有効にすべき設定は？",
                        "ハイブリッド接続とDNS"
                    ]
                },
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS)",
                    "id": "Q11",
                    "title": "Q11. Direct ConnectとMTUブラックホール",
                    "content": [
                        "状況: DX経由でPingは通るが、大きなファイルの転送やSSH接続がハングする。",
                        "問: 経路上のMTUサイズ不一致（Jumbo Frame等）と、ICMPパケットがフィルタされている場合にPath MTU Discovery (PMTUD)が失敗して起きる現象名は？"
                    ]
                },
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS)",
                    "id": "Q12",
                    "title": "Q12. BGPフラッピング",
                    "content": [
                        "状況: VPN/DX接続が数分おきに切断・再接続を繰り返す。",
                        "問: ルーターログに見られる「Hold Timer Expired」の意味と、不安定な回線においてBGPのKeepalive/Hold Timeをどう調整すべきか？"
                    ]
                },
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS)",
                    "id": "Q13",
                    "title": "Q13. NAT Gatewayのポート枯渇",
                    "content": [
                        "状況: プライベートサブネットから外部への接続が断続的に失敗。NAT GWのErrorPortAllocationが増加。",
                        "問: 何が枯渇しているか？S3/DynamoDBへのアクセスが原因の場合の解決策は？"
                    ]
                },
                {
                    "section": "2. ネットワーキング(VPC, ELB, DX, DNS)",
                    "id": "Q14",
                    "title": "Q14. Route 53 プライベートホストゾーンの解決",
                    "content": [
                        "状況: VPCピアリング先のVPCにあるプライベートホストゾーンの名前解決ができない。",
                        "問: ピアリング接続設定で有効にすべきオプションと、ホストゾーン自体に相手側VPCに対して行うべき操作は？",
                        "焦点: スケーリングの限界、整合性モデル、障害の連鎖。",
                        "RDS & Aurora"
                    ]
                }
            ],
            "3. データベース & ストレージ (RDS, DynamoDB, S3)": [
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3) - 上級編",
                    "id": "Q7",
                    "title": "Q7. RDS/Auroraのコネクション管理・RDS Proxy・Pinning問題",
                    "content": [
                        "PHP/LaravelアプリケーションをLambdaやFargateで大規模にスケールさせた結果、RDS (MySQL) が Too many connections でダウンした。対策として RDS Proxy を導入したが、期待したほど接続数が減らず、逆にパフォーマンスが低下したように見える。調査の結果、特定のクエリ実行時に「Pinning（ピン留め）」が発生していることが判明した。",
                        "Challenge:",
                        "max_connections パラメータがインスタンスクラスのメモリ容量に依存する理由と、メモリ枯渇が招くDBプロセスの挙動（OOM Killer等）を説明せよ。",
                        "RDS Proxyが提供する「コネクション多重化（Multiplexing）」の仕組みと、「Pinning（ピン留め）」が発生する具体的な条件（例：SETコマンド、テンポラリテーブル等）、およびそれが多重化効率を劇的に下げる理由を解説せよ。",
                        "RDS Proxyを使用することで、DBフェイルオーバー時のアプリケーションへの影響（DNS TTL待ち時間や接続エラー）をどう最小化できるか？",
                        "Core Knowledge & Tech Lead's View:",
                        "メモリと接続数:",
                        "MySQLは1接続ごとにスレッドスタックやバッファメモリを消費する。メモリ限界を超えるとスワップが発生し激重になるか、OOM Killerによりmysqldが殺される。",
                        "RDS ProxyとPinning:",
                        "通常、Proxyは大量のアプリ接続を少数のDB接続に集約（使い回し）する。",
                        "Pinning: 特定の条件（セッション変数の変更 SET @x=1、一時テーブルの作成、ユーザー定義変数の使用など）が発生すると、Proxyはそのセッションの整合性を保つため、そのアプリ接続を特定のDB接続に固定（ピン留め）してしまう。",
                        "ピン留めされた接続は他のリクエストで再利用できなくなるため、多重化の効果が消え、接続数が減らなくなる。アプリ側のコード修正で不要なSET等を排除する必要がある。",
                        "フェイルオーバー高速化:",
                        "RDS ProxyはDBの裏側でWriterの変更を検知し、アプリとの接続は維持したまま、バックエンドの接続先を新Writerへ切り替える。アプリはDNS更新や接続断を意識せず、一時的な待機だけで処理を継続できる（透過的フェイルオーバー）。"
                    ]
                },
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3) - 上級編",
                    "id": "Q8",
                    "title": "Q8. DynamoDBのホットパーティションと適応型キャパシティ",
                    "content": [
                        "DynamoDBを使用するソーシャルゲームで、特定の人気イベントIDにアクセスが集中し、ProvisionedThroughputExceededException が多発している。テーブル全体のキャパシティには余裕がある。AWSドキュメントには「適応型キャパシティ（Adaptive Capacity）が自動で偏りを解消する」とあるが、スロットリングが収まらない。",
                        "Challenge:",
                        "DynamoDBの1パーティションあたりの物理ハードリミット（3,000 RCU / 1,000 WCU / 10GB）を挙げ、これを超えるアクセスはAdaptive Capacityでも救えない理由を説明せよ。",
                        "Adaptive Capacityが有効になるまでのタイムラグ（反応速度）と、それが「瞬間的なスパイク」に対して無力である理由を述べよ。",
                        "ホットパーティション問題を根本解決するためのキー設計戦略（Write Sharding / Random Suffix）と、読み込み時のScatter-Gatherパターンのデメリットについて論ぜよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "物理の壁:",
                        "Adaptive Capacityは、他のパーティションの余剰分をホットなパーティションに回す機能だが、単一の物理パーティションの上限（3,000 RCU / 1,000 WCU）を超えて処理させることは物理的に不可能。",
                        "特定のアイテム（単一のPK）へのアクセス集中は、必ず単一パーティションへの負荷になるため、ここがボトルネックになる。",
                        "Adaptive Capacityの限界:",
                        "以前より高速化したが、反応には数分〜程度の時間がかかる場合がある。秒単位のスパイク（Thundering Herd）には追いつかずスロットリングが発生する。",
                        "Sharding戦略:",
                        "解決策はアクセスを散らすこと。Partition Keyに _1, _2 ... _N のような乱数サフィックスをつけて書き込む（Write Sharding）。",
                        "読むときは、全サフィックス分（N回）並列クエリを投げて集約（Scatter-Gather）する必要があり、アプリの実装コストとReadコストが増加するトレードオフがある。"
                    ]
                },
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3) - 上級編",
                    "id": "Q9",
                    "title": "Q9. Aurora Global Databaseとレプリケーション遅延・書き込み戦略",
                    "content": [
                        "Aurora (MySQL) Global Databaseを使用し、東京（Primary）と大阪（Secondary）でDR構成を組んでいる。大阪リージョンのReaderからデータを読み込む際、東京でコミットされた直後のデータが見つからない事例がある。また、大阪リージョンから直接書き込みを行いたい要件が出てきた。",
                        "Challenge:",
                        "Auroraのストレージレイヤーにおける物理レプリケーション（Quorumモデル）と、Readerノードのページキャッシュ更新ラグによるレプリケーション遅延（数ミリ〜数十ミリ秒）のメカニズムを解説せよ。",
                        "Global DatabaseにおけるGlobal Write Forwarding（書き込み転送）機能の概要と、これを利用した際の整合性モデル（Read-after-Writeの一貫性は保証されるか？）について述べよ。",
                        "Global Databaseのフェイルオーバー（RTO）が、通常のクロスリージョンレプリケーションより劇的に速い（通常1分以内）理由を、ストレージレプリケーションの仕組みから説明せよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "Auroraの遅延:",
                        "ストレージは共有されているが、Readerノードは自身のメモリ（ページキャッシュ）にデータをキャッシュしている。Writerからの「更新したよ」という無効化信号を受け取ってキャッシュを更新するまでの僅かなタイムラグが、Auroraのレプリカ遅延の正体。",
                        "Global Write Forwarding:",
                        "SecondaryリージョンのReaderで書き込みリクエストを受け取り、AWSバックボーン経由でPrimaryリージョンのWriterへ転送・実行する機能。",
                        "アプリはリージョンを意識せず書き込めるが、「書き込んだデータが即座にローカル（Secondary）のReaderで読める保証はない」（結果整合性）。書き込み完了後にレプリケーションが戻ってくるまでの遅延があるため。",
                        "高速なRTO:",
                        "Global Databaseはストレージレベルで物理ブロックを非同期転送しているため、論理レプリケーション（Binlog）よりも高速かつ低負荷。昇格（Promote）操作もストレージの役割変更だけで済むため速い。"
                    ]
                },
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3)",
                    "id": "Q15",
                    "title": "Q15. RDS Max Connections",
                    "content": [
                        "状況: 「Too many connections」エラー。",
                        "問: max_connectionsパラメータのデフォルト値は何に基づいているか？アプリケーション側でコネクションプーリングが必要な理由は？"
                    ]
                },
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3)",
                    "id": "Q16",
                    "title": "Q16. AuroraのフェイルオーバーとDNSキャッシュ",
                    "content": [
                        "状況: Auroraがフェイルオーバーしたが、アプリが古いライターへ接続を試み続けてエラーになる。",
                        "問: JavaなどのクライアントにおけるDNSキャッシュ（TTL）設定の問題点は？",
                        "DynamoDB"
                    ]
                },
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3)",
                    "id": "Q17",
                    "title": "Q17. ホットパーティション問題",
                    "content": [
                        "状況: 全体のキャパシティには余裕があるのに、特定キーへのアクセスでスロットリング発生。",
                        "問: パーティションキーの設計におけるカーディナリティ（偏り）の問題とは何か？また、Adaptive Capacity（適応型キャパシティ）が効くまでのタイムラグについて説明せよ。"
                    ]
                },
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3)",
                    "id": "Q18",
                    "title": "Q18. メタデータサービスとゴシッププロトコル",
                    "content": [
                        "状況: テーブル数やノード数が爆発的に増えた際、メタデータ管理システムが高負荷に陥る。",
                        "問: ノード間での状態共有（Membership）に使われるプロトコル名と、障害時にそれが引き起こすトラフィック増大（Storm）について説明せよ。",
                        "S3 & CloudFront"
                    ]
                },
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3)",
                    "id": "Q19",
                    "title": "Q19. S3の503 Slow Down",
                    "content": [
                        "状況: S3への大量のPUT/GETリクエストで503エラーが返る。",
                        "問: S3のパフォーマンスはバケット全体ではなく何単位で制限されるか？また、プレフィックスごとのリクエスト上限について答えよ。"
                    ]
                },
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3)",
                    "id": "Q20",
                    "title": "Q20. S3の整合性モデル（過去と現在）",
                    "content": [
                        "状況: PUT直後のGETで404になる（以前のS3）。",
                        "問: 現在のS3は強い整合性（Strong Consistency）をサポートしているが、かつての結果整合性（Eventual Consistency）時代に必要だったアプリケーション側の対策は？"
                    ]
                },
                {
                    "section": "3. データベース & ストレージ (RDS, DynamoDB, S3)",
                    "id": "Q21",
                    "title": "Q21. CloudFrontの古いコンテンツ（キャッシュ無効化）",
                    "content": [
                        "状況: S3上の静的ファイルを更新したが、ユーザーには古い画像が表示され続けている。",
                        "問: CloudFrontのエッジキャッシュを強制的に更新するために実行すべき操作（Invalidation）と、再発防止のための適切なキャッシュ戦略（ファイル名バージョニング等）について説明せよ。",
                        "焦点: 隠れたリソース制限、起動の失敗要因。",
                        "Lambda"
                    ]
                }
            ],
            "4. サーバーレス & コンテナ (Lambda, ECS, EKS)": [
                {
                    "section": "4. サーバーレス & コンテナ (Lambda, ECS, EKS) - 上級編",
                    "id": "Q10",
                    "title": "Q10. Lambda Cold Start & Concurrency Model (SnapStart)",
                    "content": [
                        "Javaで実装されたLambda関数があり、API Gateway経由で呼び出されている。不定期なアクセススパイク時に、極端なレイテンシ悪化（コールドスタート）と ThrottlingException (429) が同時に発生している。アカウントの同時実行数上限には余裕がある。",
                        "Challenge:",
                        "LambdaのBurst Concurrency（バースト同時実行数）の制限について、リージョンごとの初期バースト値（東京: 1,000など）と、それを超えた場合のスケーリング速度（毎分500インスタンス追加）の仕様を解説せよ。",
                        "Javaランタイム特有の重いコールドスタートを解消するための Lambda SnapStart の仕組み（CRaC: Checkpoint/Restore in Userspace）と、プロビジョニング済み同時実行（Provisioned Concurrency）との使い分け基準を述べよ。",
                        "Provisioned Concurrency を設定しているにもかかわらず、デプロイ直後や設定変更直後にスパイクが来るとスロットリングが発生する「初期化ラグ」の問題について触れよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "Burst Limit:",
                        "アカウント上限（例: 10,000）があっても、一気に10,000まで増えるわけではない。",
                        "初期バースト（東京なら1,000）までは即座に増えるが、それ以降は 毎分500 ずつしかスケールしない。これを超える急激なスパイクは429エラーになる。",
                        "SnapStart vs Provisioned:",
                        "SnapStart: 初期化済みメモリ状態（Firecracker microVMのスナップショット）から復元して起動。無料で使える（Javaのみ）。コールドスタートを劇的に短縮するが、常時起動しているわけではない（Scale to Zero可能）。",
                        "Provisioned Concurrency: 常に指定数のWarmインスタンスを維持する（有料）。バースト制限やコールドスタートを完全に排除したい場合に必須。",
                        "初期化ラグ:",
                        "Provisioned Concurrencyの設定が完了するまで（Warm Poolが埋まるまで）数分かかる。デプロイ直後はここが弱点になりうる。"
                    ]
                },
                {
                    "section": "4. サーバーレス & コンテナ (Lambda, ECS, EKS) - 上級編",
                    "id": "Q11",
                    "title": "Q11. SQS + Lambda: Partial Failure & Poison Pill",
                    "content": [
                        "SQSをイベントソースとしてLambdaをトリガーしている。バッチサイズを10に設定しているが、そのうち1件のメッセージ処理だけがデータ不備でエラーになる。しかし、Lambda全体が失敗とみなされ、残りの正常な9件も含めて再処理（リトライ）が繰り返されている。",
                        "Challenge:",
                        "SQSトリガーのLambdaにおける「バッチ全体の失敗」のデフォルト挙動と、それを防ぐために実装すべき ReportBatchItemFailures（部分バッチ応答）の仕組みをコードレベルの返り値構造で説明せよ。",
                        "エラーになり続けるメッセージ（Poison Pill）が無限リトライされるのを防ぐための maxReceiveCount と DLQ (Dead Letter Queue) の正しい設定関係を述べよ。",
                        "Lambdaの非同期呼び出し（Event Invoke）におけるDLQ/Destinationsと、SQSトリガー（Sync Invoke扱い）におけるDLQの違いを明確にせよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "ReportBatchItemFailures:",
                        "デフォルトでは、Lambdaが例外を投げるとバッチ全体（10件）がSQSに戻され、全て再処理される。",
                        "レスポンスに {\"batchItemFailures\": [{\"itemIdentifier\": \"message-id\"}]} を含めることで、失敗した特定のメッセージだけをSQSに残し、成功したメッセージは削除（Commit）させることができる。",
                        "DLQ設定:",
                        "SQS側でRedrive Policyを設定。maxReceiveCount（例: 3回）を超えたらDLQ用キューへ移動させる。",
                        "Invoke Modeの違い:",
                        "SQSトリガーは、Lambdaサービスがポーリングして関数を同期的に実行する。よってLambda関数のDLQ設定ではなく、SQSキューのDLQ設定が効く。",
                        "非同期呼び出し（S3通知等）の場合は、Lambda関数自体のDLQ/Destinations設定が使われる。"
                    ]
                },
                {
                    "section": "4. サーバーレス & コンテナ (Lambda, ECS, EKS) - 上級編",
                    "id": "Q12",
                    "title": "Q12. EKS IP Exhaustion & Fargate Profiles",
                    "content": [
                        "EKSクラスタで大量のPodを起動しようとしたところ、ノードのリソースは余っているのにIPアドレス不足でPodがPendingになった。サブネットのCIDRは/24で枯渇している。ノードを増やすこともできない。",
                        "Challenge:",
                        "VPC CNIプラグインの Warm IP / Warm ENI 戦略が、なぜIPアドレスを大量に（Pod数以上に）消費してしまうのか説明せよ。",
                        "この問題を解決するための Prefix Delegation (/28割当て) 機能の概要と、これにより1つのENIで扱えるIP数がどう変化するか述べよ。",
                        "EKS Fargate を利用する場合のIPアドレス消費モデル（PodごとのVM占有）と、EC2ノード運用と比較した際のコスト・制約（DaemonSet不可など）のトレードオフを論ぜよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "Warm IP:",
                        "高速起動のため、VPC CNIはENIに付与可能なIPをあらかじめ確保（プール）しておく。デフォルトではENIの限界までIPを確保しようとするため、サブネットIPを食いつぶす。",
                        "Prefix Delegation:",
                        "ENIに個別のIPではなく、/28 プレフィックス（16個のIPブロック） を割り当てる。",
                        "1回のAPIコールで16個分のIP枠を確保でき、IP枯渇問題とAPIスロットリング問題を同時に緩和できる。",
                        "Fargateの特性:",
                        "Fargate Podは1つ1つが個別のMicroVMで動作し、個別のENIを持つ。つまりPod数 = IP消費数となる。",
                        "DaemonSetが使えないため、ログ収集や監視のエージェントをサイドカーとして全Podに入れる必要があり、リソース効率が悪化する場合がある。"
                    ]
                },
                {
                    "section": "4. サーバーレス & コンテナ (Lambda, ECS, EKS)",
                    "id": "Q22",
                    "title": "Q22. 同時実行数とスロットリング",
                    "content": [
                        "状況: Lambdaが429エラー。アカウント上限（1000等）には達していない。",
                        "問: バースト同時実行数（Burst Concurrency）の制限（リージョンごとの初期バースト値とスケーリング速度）について説明せよ。"
                    ]
                },
                {
                    "section": "4. サーバーレス & コンテナ (Lambda, ECS, EKS)",
                    "id": "Q23",
                    "title": "Q23. VPC LambdaとENI（Hyperplaneの理解）",
                    "content": [
                        "状況: VPC Lambdaの接続数が増えるとIPアドレスが枯渇する懸念。",
                        "問: 以前の仕様と異なり、現在のHyperplane ENIはどのようにENIを共有するか？それでもIP枯渇が起きるケースは？"
                    ]
                },
                {
                    "section": "4. サーバーレス & コンテナ (Lambda, ECS, EKS)",
                    "id": "Q24",
                    "title": "Q24. 非同期呼び出しとリトライストーム",
                    "content": [
                        "状況: S3トリガーのLambdaがエラーになり続け、ログが爆発的に増えている。",
                        "問: 非同期呼び出しの自動リトライ仕様（2回+キュー滞留）と、DLQ（デッドレターキュー）を設定していない場合のリスクは？",
                        "コンテナ (ECS/EKS)"
                    ]
                },
                {
                    "section": "4. サーバーレス & コンテナ (Lambda, ECS, EKS)",
                    "id": "Q25",
                    "title": "Q25. EKS IP枯渇とCNIプラグイン",
                    "content": [
                        "状況: EKSでPodがPendingのまま。ノードのリソースは余っている。",
                        "問: AWS VPC CNIプラグインのデフォルト挙動（Warm IP）が、どのようにサブネットのIPアドレスを大量消費するか？"
                    ]
                },
                {
                    "section": "4. サーバーレス & コンテナ (Lambda, ECS, EKS)",
                    "id": "Q26",
                    "title": "Q26. ECSタスク起動失敗とイメージプル",
                    "content": [
                        "状況: FargateタスクがPENDING -> STOPPEDを繰り返す。",
                        "問: プライベートサブネットでNAT GWがない場合、ECRからイメージをプルできるか？必要なVPCエンドポイントは？"
                    ]
                },
                {
                    "section": "4. サーバーレス & コンテナ (Lambda, ECS, EKS)",
                    "id": "Q27",
                    "title": "Q27. CrashLoopBackOffの調査",
                    "content": [
                        "状況: Podが再起動を繰り返す。現在のログを見ても何も出ていない。",
                        "問: 直前のクラッシュ時のログを見るためのkubectlオプションは？",
                        "焦点: 権限不足の特定、IAMロールの仕様。"
                    ]
                }
            ],
            "5. IAM & セキュリティのトラブルシューティング": [
                {
                    "section": "5. IAM & セキュリティのトラブルシューティング - 上級編",
                    "id": "Q13",
                    "title": "Q13. Circuit Breaker & Bulkhead Patterns",
                    "content": [
                        "外部の決済APIが遅延し始め、呼び出し元のECSサービスの全スレッドが待機状態（Blocked）になり、ヘルスチェックすら応答できずにシステムダウン（Cascading Failure）した。再起動しても即座にまた詰まる。",
                        "Challenge:",
                        "Circuit Breaker パターンの3状態（Closed、 Open, Half-Open）の遷移ロジックに加え、Fail Fast（即時失敗）がシステム全体の生存になぜ不可欠なのか解説せよ。",
                        "サーキットブレーカーだけでは防げない「リソース枯渇」に対処するための Bulkhead（隔壁）パターン の実装方法（スレッドプール分離やセマフォ分離）を述べよ。",
                        "AWS App MeshやEnvoyプロキシの Outlier Detection（外れ値検知） 機能を用いて、インフラ層でこれを自動化する方法について触れよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "Fail Fast:",
                        "ダメな時は待たずに即エラーを返すこと。タイムアウトまで待つ（ブロッキングする）時間が、スレッドやメモリを占有し、他の健全な処理まで道連れにする。",
                        "Bulkhead:",
                        "船の隔壁のようにリソースを区切る。決済API用のスレッドプールと、ヘルスチェック/Topページ用のスレッドプールを分ける。これにより決済APIが死んでもTopページは生き残る。",
                        "Outlier Detection:",
                        "Envoyなどのプロキシが、連続して5xxを返すアップストリームホストを一時的に切り離す（Ejection）機能。アプリコードを変更せずにサーキットブレーカー相当の動きを実現できる。"
                    ]
                },
                {
                    "section": "5. IAM & セキュリティのトラブルシューティング - 上級編",
                    "id": "Q14",
                    "title": "Q14. Static Stability & Route 53 ARC",
                    "content": [
                        "AWSのリージョン規模の障害（Control Plane障害）が発生し、EC2の新規起動やAuto Scaling、Route 53のAPI変更ができない状況に陥った。しかし、経営陣は「稼働中のリソースだけでサービスを継続せよ」と要求している。",
                        "Challenge:",
                        "Static Stability（静的安定性） の概念を定義し、障害発生時に「コントロールプレーン（設定変更）」に依存しないアーキテクチャがいかにして可用性を高めるか説明せよ。",
                        "Route 53 Application Recovery Controller (ARC) の機能（ゾーンシフトやルーティングコントロール）が、従来のヘルスチェックベースのDNSフェイルオーバーと比べて、なぜより確実な復旧手段となり得るのか論ぜよ。",
                        "静的安定性を実現するためのコスト（Over-provisioning）は「保険料」であるが、リザーブドインスタンスやSavings Plans、Spot Instancesをどう組み合わせればコストを最適化しつつ冗長性を維持できるか？",
                        "Core Knowledge & Tech Lead's View:",
                        "Static Stability:",
                        "「障害が起きてからスケールする（Reactive）」のではなく、「障害が起きてもそのままで耐えられる」状態。",
                        "例: 3AZ構成で1AZがダウンしても、残りの2AZだけでトラフィックを捌けるよう、平時から50%余分に（合計150%の）リソースを稼働させておく。",
                        "障害時はAPI（RunInstances）自体が失敗する可能性が高いため、既存のリソース（Data Plane）だけで戦うのが最強。",
                        "Route 53 ARC:",
                        "ヘルスチェックは「偽陽性（False Positive）」や「フラッピング」のリスクがある。",
                        "ARCは、人間または自動システムが明示的に「スイッチを切り替える」ことで、DNSの重み付けを安全かつ確実に変更する仕組み。コントロールプレーンの依存を排除した特殊なデータプレーンで動作する。"
                    ]
                },
                {
                    "section": "5. IAM & セキュリティのトラブルシューティング - 上級編",
                    "id": "Q15",
                    "title": "Q15. Thundering Herd & Jitter / Idempotency",
                    "content": [
                        "大規模障害から復旧した瞬間、数百万のクライアントが一斉に再接続（Reconnect）を試み、データベースとロードバランサーが即死した（Thundering Herd問題）。また、リトライによって二重決済が発生している。",
                        "Challenge:",
                        "クライアント側のリトライロジックにおける Exponential Backoff だけでは不十分で、Jitter（ゆらぎ） を加えることが数学的に必須である理由を説明せよ。",
                        "分散システムにおける 冪等性（Idempotency） の担保戦略として、APIリクエストに含めるべき Idempotency Key の役割と、サーバー側（DynamoDBやRedis）での実装パターン（TTL付きロック等）を設計せよ。",
                        "サーバー側での防御策としての Load Shedding（負荷制限・切り捨て） の重要性と、AWS WAFやAPI Gatewayでの実装例を挙げよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "Jitter:",
                        "指数バックオフ（1秒, 2秒, 4秒...）だけだと、全員が同じタイミングで待って同じタイミングで再試行するため、負荷の「波」が消えない。",
                        "ランダムな時間を加える（Jitter）ことで、アクセスを時間の軸で平準化・分散させる。",
                        "Idempotency Key:",
                        "クライアントがリクエスト時に一意なID（UUID等）を付与。",
                        "サーバーは「このIDは処理済みか？」をKVS等で確認。処理済みなら実際の処理をスキップして、前回と同じ成功レスポンスを返す。",
                        "これにより、タイムアウト時のリトライによる二重処理（二重課金）を安全に防げる。"
                    ]
                },
                {
                    "section": "5. IAM & セキュリティのトラブルシューティング - 上級編",
                    "id": "Q16",
                    "title": "Q16. Blast Radius & Cellular Architecture",
                    "content": [
                        "ある一人のヘビーユーザー（または設定ミスのテナント）が共有リソースを食いつぶし、全ユーザーに影響が出る大規模障害が発生した。これを防ぐために Cell-based Architecture（セルラーアーキテクチャ） への移行を検討している。",
                        "Challenge:",
                        "Cellular Architecture の基本概念と、シャーディング（DB分割）との決定的な違い（スタック全体の垂直分割）を説明せよ。",
                        "セルラー構成における Routing Layer（薄いルーティング層） の設計課題と、Route 53やCloudFront Functionsを用いてユーザーを正しいセルに導く方法を提案せよ。",
                        "セルラーアーキテクチャが Blast Radius（爆発半径） を最小化するメカニズムと、デプロイメントの安全性（1セルずつデプロイ）への寄与について論ぜよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "Cellular Architecture:",
                        "システム全体（LB、 Web、 App, DB、 Queue）を独立した「セル」という単位に分割して並列化する。",
                        "シャーディングはDBだけだが、セルは全スタックを隔離する。あるセルが死んでも、影響はそのセル内のユーザー（例: 全体の5%）に限定される。",
                        "Routing:",
                        "「誰がどのセルにいるか」を知るためのマッピングが必要。",
                        "最も堅牢なのは、計算不要な静的なパーティション（例：ユーザーIDのハッシュ値）を使い、Route 53やCloudFront Edgeで振り分ける方法。ルーティング層自体がSPOFにならないように極限までシンプルにする（Simple is reliable）。"
                    ]
                },
                {
                    "section": "5. IAM & セキュリティのトラブルシューティング",
                    "id": "Q28",
                    "title": "Q28. 権限不足のデバッグ",
                    "content": [
                        "状況: アプリケーションがS3へのアクセスでAccess Deniedになる。",
                        "問: CloudTrailで該当のAPIコールを検索し、どのポリシー（アイデンティティベース、リソースベース、SCP）が拒否しているか特定する手順は？"
                    ]
                },
                {
                    "section": "5. IAM & セキュリティのトラブルシューティング",
                    "id": "Q29",
                    "title": "Q29. iam:PassRole",
                    "content": [
                        "状況: EC2インスタンスを起動する権限はあるが、インスタンスにIAMロールを割り当てようとするとエラーになる。",
                        "問: ロールをAWSサービスに渡すためのiam:PassRole権限の必要性について説明せよ。",
                        "焦点: 過去のPost-Mortemから学ぶ、カスケード障害と静的安定性。",
                        "過去の大規模障害から学ぶ"
                    ]
                }
            ],
            "6. 大規模障害ケーススタディ & レジリエンス": [
                {
                    "section": "6. 大規模障害ケーススタディ & レジリエンス",
                    "id": "Q17",
                    "title": "Q17. S3 Strong Consistency & Data Lake Performance",
                    "content": [
                        "S3をデータレイクとして使用し、Athenaで分析している。以前は「書き込み直後の読み込み」でデータが見えない問題（結果整合性）があったが、現在は解消されているはずだ。しかし、大量の小さなファイルをPUTした直後にLIST操作を行うとパフォーマンスが出ない。",
                        "Challenge:",
                        "現在のS3が提供する Strong Consistency（強い整合性） の仕様（PUT/DELETE後のREAD/LIST）について、正確に述べよ。",
                        "S3のパフォーマンスにおける Prefix（プレフィックス） の重要性と、かつて必要だった「ハッシュ化プレフィックス」が現在では不要になった理由、および現在のスケーリング仕様（1プレフィックスあたりのTPS: 3,500 PUT / 5,500 GET）を解説せよ。",
                        "大量の小ファイル問題（Small File Problem）がAthena/Sparkのパフォーマンスに与える悪影響と、これを解決するための S3 DistCp やETL処理でのファイル結合（Compaction）の重要性を説け。",
                        "Core Knowledge & Tech Lead's View:",
                        "Strong Consistency: 2020年末より、S3は全てのPUT/DELETE操作に対して強い整合性を持つようになった。書き込み直後のGETやLISTは常に最新の結果を返す。",
                        "Partitioning: S3は自動的にプレフィックスに基づいてパーティションを分割・スケールさせる。現在はハッシュ化不要で、順次プレフィックス（日付等）でも自動でスケールするが、急激なスパイクには 503 Slow Down が出る場合がある。",
                        "Small Files: S3/Athenaは数KBのファイルを数百万個読むのが苦手（APIコール数とレイテンシのオーバーヘッド）。MB〜GB単位にまとめる（Compaction）のが鉄則。"
                    ]
                },
                {
                    "section": "6. 大規模障害ケーススタディ & レジリエンス",
                    "id": "Q18",
                    "title": "Q18. Gateway Load Balancer (GWLB) & Inspection",
                    "content": [
                        "セキュリティ要件により、VPCに出入りする全トラフィックをサードパーティ製のファイアウォールアプライアンス（Palo Alto、 FortiGate等）で検査したい。従来はTGWやVPN接続が必要だったが、構成が複雑でボトルネックになりやすい。",
                        "Challenge:",
                        "Gateway Load Balancer (GWLB) が提供する「Bump-in-the-wire（透過的検査）」アーキテクチャの仕組みを、GENEVEプロトコルとルートテーブルのターゲット指定（Gateway Load Balancer Endpoint: GWLBE）を用いて解説せよ。",
                        "GWLBを使用することで、アプライアンスのオートスケーリングやヘルスチェックが容易になる理由を、従来のEC2ベースのFW構成と比較して述べよ。",
                        "Ingress Routing（インターネットからの流入）において、Internet Gateway (IGW) のルートテーブルで Ingress Routing（Edge Association） を設定し、トラフィックをGWLBEに強制的に引き込む手法を説明せよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "GWLB: L3（ネットワーク層）で動作し、パケットをカプセル化（GENEVE）して裏側のFWフリートに投げる。FWはパケットを検査してそのまま返す。",
                        "透過性: アプリ側や通信相手からは、間にGWLB/FWがいることは見えない（IPが変わらない）。NATも不要。",
                        "Ingress Routing: IGWに関連付けたルートテーブルで、Dest: Subnet-CIDR -> Target: GWLBE と書くことで、外から入ってきたパケットを強制的に検査装置へねじ曲げることができる。"
                    ]
                },
                {
                    "section": "6. 大規模障害ケーススタディ & レジリエンス",
                    "id": "Q19",
                    "title": "Q19. Container Insights & Observability",
                    "content": [
                        "EKS上でマイクロサービスを運用しているが、PodがOOMKilled（メモリ不足で強制終了）されていることに気づくのが遅れた。CloudWatchの標準メトリクスではノード全体のCPU/メモリしか見えず、Pod単位の特定が困難である。",
                        "Challenge:",
                        "CloudWatch Container Insights を有効化することで収集されるメトリクスの粒度（Cluster、 Node、 Pod、 Service）と、その背後で動くエージェント（CloudWatch Agent / Fluent Bit）の役割を説明せよ。",
                        "OOMKilled のようなイベントを即座に検知するために、Container Insightsのメトリクス（pod_memory_utilization等）やログパターン監視（Reason: OOMKilled）をどう設定すべきか。",
                        "プロメテウス（Amazon Managed Service for Prometheus）とGrafanaを用いたOSSベースの監視スタックと、Container Insightsの使い分け（コスト、手軽さ、詳細度）についてTech Leadとしての推奨を述べよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "Container Insights: Fluent Bit等がコンテナランタイムやkubeletから詳細情報を吸い上げ、構造化データとしてCloudWatchに送る。Pod単位のリソース使用率が見えるようになる。",
                        "OOM検知: メモリ使用率監視だけでは不十分（スパイクで死ぬため）。K8sイベントログやアプリログで OOMKilled 文字列を監視し、アラートを飛ばすのが確実。",
                        "Prometheus vs CW: 大規模クラスタで全PodのメトリクスをCWに送るとコストが爆発する（Custom Metrics課金）。大規模環境ではPrometheusの方が安価で柔軟な場合が多い。小規模ならCW Container Insightsが手軽。"
                    ]
                },
                {
                    "section": "6. 大規模障害ケーススタディ & レジリエンス",
                    "id": "Q20",
                    "title": "Q20. Security Hub & GuardDuty: Continuous Compliance",
                    "content": [
                        "複数のAWSアカウントを持つ組織で、セキュリティ基準（PCI DSSやCIS Benchmark）の遵守状況を可視化したい。また、アクセスキーの漏洩やコインマイニングなどの脅威をリアルタイムで検知したい。",
                        "Challenge:",
                        "Amazon GuardDuty が検知できる脅威の種類（VPC Flow Logs、 CloudTrail、 DNS Logsの分析）と、これがエージェントレスで動作するメリットを述べよ。",
                        "AWS Security Hub が提供する「一元管理」と「自動修復（Automated Remediation）」の機能を、EventBridgeとLambdaを組み合わせたアーキテクチャで説明せよ（例：意図しないSG開放を検知して即座に閉じる）。",
                        "組織全体（AWS Organizations）でこれらのセキュリティサービスを有効化する際のベストプラクティス（委任管理者: Delegated Administratorの設定）について触れよ。",
                        "Core Knowledge & Tech Lead's View:",
                        "GuardDuty: ログを機械学習で分析し、異常な通信（C&Cサーバーへの接続）やIAMの異常なAPIコールを検知。エージェント不要なので全アカウントで即ONにすべき（必須）。",
                        "Security Hub: 各種セキュリティサービス（GuardDuty、 Inspector, Macie）のアラートを集約し、CISベンチマーク等のスコアを表示する。",
                        "自動修復: Security Hubの検知イベント -> EventBridge -> Lambda で、「SGの22番ポート開放"
                    ]
                },
                {
                    "section": "6. 大規模障害ケーススタディ & レジリエンス (SRE/Principal)",
                    "id": "Q30",
                    "title": "Q30. 2020年 Kinesis障害とカスケード",
                    "content": [
                        "状況: Kinesisの障害により、CognitoやCloudWatch、Auto Scalingまでもが連鎖的に機能不全に陥った。",
                        "問: なぜKinesisの障害が他のサービスに波及したのか？「フリート全体の最大スレッド数超過」と「循環依存」の観点から説明せよ。"
                    ]
                },
                {
                    "section": "6. 大規模障害ケーススタディ & レジリエンス (SRE/Principal)",
                    "id": "Q31",
                    "title": "Q31. 2017年 S3障害と爆発半径",
                    "content": [
                        "状況: コマンド入力ミスにより、想定以上のS3サブシステムサーバーが削除され、リージョン障害に発展。",
                        "問: この教訓から生まれた、運用ツールにおける「爆発半径（Blast Radius）の最小化」や「セルラーアーキテクチャ」とは？"
                    ]
                },
                {
                    "section": "6. 大規模障害ケーススタディ & レジリエンス (SRE/Principal)",
                    "id": "Q32",
                    "title": "Q32. 2021年 US-EAST-1障害と内部DNS",
                    "content": [
                        "状況: 内部ネットワークの輻輳により、AWS内部DNSの解決が失敗し、APIエラーが多発。",
                        "問: サービス間通信においてDNS解決に依存することのリスクと、データプレーンの静的安定性（Static Stability）の重要性は？",
                        "運用戦略"
                    ]
                },
                {
                    "section": "6. 大規模障害ケーススタディ & レジリエンス (SRE/Principal)",
                    "id": "Q33",
                    "title": "Q33. Thundering Herd（再開の波）対策",
                    "content": [
                        "状況: 障害復旧直後、待機していたリクエストが一斉に殺到し、DBが再度ダウン（ブラウンアウト）。",
                        "問: クライアント側のリトライロジックに入れるべきExponential BackoffとJitter（ゆらぎ）の効果は？"
                    ]
                },
                {
                    "section": "6. 大規模障害ケーススタディ & レジリエンス (SRE/Principal)",
                    "id": "Q34",
                    "title": "Q34. サーキットブレーカー",
                    "content": [
                        "状況: 依存する外部APIが遅延し、自システムの全スレッドが待機状態で埋め尽くされた。",
                        "問: 障害のある依存先を即座に切り離し、即時エラーを返すことで自システムを守るデザインパターンは？",
                        "焦点: 見落としがちな仕様、泥臭い運用回避策。"
                    ]
                }
            ],
            "7. その他・運用Tips (Cost, Ops)": [
                {
                    "section": "7. その他・運用Tips (Cost, Ops)",
                    "id": "Q35",
                    "title": "Q35. Windows RDPパスワード取得不可",
                    "content": [
                        "状況: Windowsインスタンス起動後、「パスワードはまだ使用できません」と表示され続ける。",
                        "問: インスタンス内部で動いている、パスワード生成に必要な初期化サービスの名前は？"
                    ]
                },
                {
                    "section": "7. その他・運用Tips (Cost, Ops)",
                    "id": "Q36",
                    "title": "Q36. サポートケース起票の鉄則",
                    "content": [
                        "状況: 技術サポートに調査を依頼するが、解決が遅い。",
                        "問: 初回の問い合わせで必ず含めるべき、調査時間を短縮するための3つの具体的情報は？"
                    ]
                },
                {
                    "section": "7. その他・運用Tips (Cost, Ops)",
                    "id": "Q37",
                    "title": "Q37. 終了保護の罠",
                    "content": [
                        "状況: 終了保護（Termination Protection）を有効にしたインスタンスが、Auto Scalingのスケールイン時に削除されてしまった。",
                        "問: なぜか？ASG側で設定すべき項目は？"
                    ]
                },
                {
                    "section": "7. その他・運用Tips (Cost, Ops)",
                    "id": "Q38",
                    "title": "Q38. コスト急増の犯人探し",
                    "content": [
                        "状況: データ転送量が急増し高額請求が来た。",
                        "問: VPCフローログ以外に、S3へのアクセス（APIコール数や転送量）を詳細に分析するために有効にする機能は？"
                    ]
                }
            ]
        };

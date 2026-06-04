/**
 * ════════════════════════════════════════════════════════════════════════════
 * js/quiz-data.js — Static Quiz Datasets (extracted from main.js, v80+ Stage 3)
 * ════════════════════════════════════════════════════════════════════════════
 *
 * @fileoverview
 * `main.js` の単一 IIFE 内に同居していた 4 つの巨大な静的データ定義を、ローカル ESM へ
 * 物理分割した（Stage 3: static data 抽出）。いずれも関数も副作用も持たない純粋なデータ
 * （ネストしたオブジェクト/配列/文字列）であり、出力も振る舞いも無い。データは読み込み
 * 順序にも DOM にもクロージャ状態にも依存しないため、別モジュールへ移しても挙動は一切
 * 変わらない。約 1,360 行を main.js から分離し、可読性と保守性を大きく改善する。
 *
 * ── 内容（4 データセット）─────────────────────────────────────────────────
 *   - awsQuizData          : AWS 問題集データ。
 *   - pmQuizData           : PM 問題集データ。
 *   - qualityQuizData      : 品質・プロセス問題集データ。
 *   - architectureQuizData : v29 意思決定問題集データ（設計判断シナリオ集）。
 * これら 4 つは main.js の quiz ソース lookup table（aws/pm/quality/architecture）から
 * 参照される。**4 つすべてを過不足なく export することが必須**（1 つでも欠けると lookup が
 * 未定義参照になり、SPA 起動時に module-load エラーで全停止する）。これは過去に「4 個中
 * 2 個しか export しない」抜けを起こしかけた箇所であり、Check 47 が main.js の import と
 * このモジュールの export の一致を BLOCKING で機械強制する。
 *
 * ── 取り扱い ───────────────────────────────────────────────────────────────
 *   - 4 データは main.js から **バイト等価** で切り出した（手入力による転記ミスを避ける
 *     ため、元ファイルの該当行をそのまま抽出して `export` を前置した）。内容の改変・要約・
 *     中立化は禁止（設問本文・意図・選択肢はプロダクトの中身であり省略しない）。
 *   - 本モジュールは依存ゼロの葉モジュール（import を持たない。Check 47c が強制）。
 *
 * ── 読み込み機構 ───────────────────────────────────────────────────────────
 * `index.html` が `main.js` を `<script type="module">` で読み込み、`main.js` が本モジュール
 * を `import` する。CSP `script-src 'self'` のため同一オリジン取得は追加設定不要。
 * ════════════════════════════════════════════════════════════════════════════
 */

'use strict';

// ───── AWS 問題集データ（main.js から byte-equivalent 抽出）─────
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

// ───── PM 問題集データ（main.js から byte-equivalent 抽出）─────
export const pmQuizData = {
            "1. 要件・意思決定": [
                {
                    "section": "1. 要件・意思決定",
                    "id": "Q1",
                    "title": "Q1. 要求が曖昧なまま始まりそうなとき",
                    "content": [
                        "新規プロジェクトのキックオフ前だが、要件が「ユーザーにとって便利な機能」というレベルに留まっている。期限は決まっている。この状態でPMは何を決め、何を決めずに進めるか。",
                        "",
                        "意図:",
                        "要件が曖昧＝止める、ではなく曖昧なままでも決められる粒度を切り出せるか。"
                    ]
                },
                {
                    "section": "1. 要件・意思決定",
                    "id": "Q2",
                    "title": "Q2. ステークホルダーの意見が割れたとき",
                    "content": [
                        "事業側はスピード重視、技術側は品質重視。両者の主張はどちらも合理的で、決定を先延ばしにすると影響が出る。PMは何を根拠に意思決定すべきか。",
                        "",
                        "意図:",
                        "調整役ではなく、決断役として立てるか。"
                    ]
                },
                {
                    "section": "1. 要件・意思決定",
                    "id": "Q3",
                    "title": "Q3. スコープ追加の要求",
                    "content": [
                        "開発後半になって、「ついでにこれも入れたい」という要望が出た。工数は小さく見えるが、影響範囲は不明。PMとしてどう判断するか。",
                        "",
                        "意図:",
                        "工数ではなく不確実性を見ているか。"
                    ]
                },
                {
                    "section": "1. 要件・意思決定",
                    "id": "Q11",
                    "title": "Q11. 判断を急がされる状況",
                    "content": [
                        "市場要因により、当初想定より1か月前倒しでのリリースを求められた。品質・スコープ・体制のいずれも余裕はない。PMとして「即断すること」と「即断しないこと」をどう分けるか。",
                        "",
                        "意図:",
                        "スピード要求下での判断の分離能力。"
                    ]
                },
                {
                    "section": "1. 要件・意思決定",
                    "id": "Q14",
                    "title": "Q14. 判断材料が足りないまま決める必要があるとき",
                    "content": [
                        "重要な意思決定だが、情報が揃うまで待つと機会を逃す。どの条件が揃った時点で決断するか。",
                        "",
                        "意図:",
                        "完全情報を前提にしない意思決定基準。"
                    ]
                }
            ],
            "2. チーム・人": [
                {
                    "section": "2. チーム・人",
                    "id": "Q5",
                    "title": "Q5. 成果が出ていないメンバーへの対応",
                    "content": [
                        "特定のメンバーのアウトプットが安定せず、チーム全体の足を引っ張り始めている。技術力・意欲・環境、原因は不明。PMとして最初に取る行動は何か。",
                        "",
                        "意図:",
                        "人を評価する前に、状況を設計し直せるか。"
                    ]
                }
            ],
            "3. プロセス・計画": [
                {
                    "section": "3. プロセス・計画",
                    "id": "Q4",
                    "title": "Q4. 失敗が見え始めたとき",
                    "content": [
                        "進捗は表面上問題ないが、チームの雰囲気やレビュー内容から、「このままだと後で崩れる」という兆候を感じている。PMはどの時点で介入するべきか。",
                        "",
                        "意図:",
                        "数値に出る前の違和感をどう扱うか。"
                    ]
                },
                {
                    "section": "3. プロセス・計画",
                    "id": "Q12",
                    "title": "Q12. 成果が測れない施策",
                    "content": [
                        "経営判断で「効果は数値化しづらいが重要」とされる施策を実施することになった。PMとして、何をもって成功・失敗を判断するか。",
                        "",
                        "意図:",
                        "KPI不在時の評価軸設計。"
                    ]
                },
                {
                    "section": "3. プロセス・計画",
                    "id": "Q13",
                    "title": "Q13. 計画が機能しなくなったとき",
                    "content": [
                        "計画は存在するが、現場が誰も参照していない状態になっている。計画を作り直すべきか、運用を変えるべきか。どう判断するか。",
                        "",
                        "意図:",
                        "計画を成果物ではなく道具として扱えるか。"
                    ]
                }
            ],
            "4. 評価・指標": [
                {
                    "section": "4. 評価・指標",
                    "id": "Q6",
                    "title": "Q6. 成功しているが違和感があるプロジェクト",
                    "content": [
                        "売上・評価ともに良好だが、チームが疲弊しており、このやり方が続くとは思えない。PMとして、この状態をどう扱うか。",
                        "",
                        "意図:",
                        "短期成功を疑えるか。"
                    ]
                },
                {
                    "section": "4. 評価・指標",
                    "id": "Q7",
                    "title": "Q7. 数値目標が逆効果になったとき",
                    "content": [
                        "KPIを設定した結果、チームが数字を達成することだけに最適化し始めた。品質や協力が下がっている。PMはKPIをどう扱うべきか。",
                        "",
                        "意図:",
                        "指標を神聖化しない判断ができるか。"
                    ]
                },
                {
                    "section": "4. 評価・指標",
                    "id": "Q10",
                    "title": "Q10. PMとしての成果の定義",
                    "content": [
                        "プロジェクトが終了した。機能はリリースされ、一定の成果も出た。PMとして、このプロジェクトの成功／失敗をどう定義するか。",
                        "",
                        "意図:",
                        "成果をアウトプット以外で語れるか。"
                    ]
                }
            ],
            "5. 技術・判断": [
                {
                    "section": "5. 技術・判断",
                    "id": "Q8",
                    "title": "Q8. 技術的判断に踏み込むべきか",
                    "content": [
                        "技術選定について、開発チーム内で意見が割れている。PMは技術の専門家ではない。どこまで踏み込み、どこから任せるべきか。",
                        "",
                        "意図:",
                        "分からないことを理由に逃げないか。"
                    ]
                },
                {
                    "section": "5. 技術・判断",
                    "id": "Q9",
                    "title": "Q9. プロジェクトを止める判断",
                    "content": [
                        "進行中のプロジェクトが、コスト・品質・市場状況の観点から見て成功確率が低下している。「止める」という判断はいつ成立するか。",
                        "",
                        "意図:",
                        "継続バイアスから自由か。"
                    ]
                }
            ],
            "6. 権限・委譲": [
                {
                    "section": "6. 権限・委譲",
                    "id": "Q15",
                    "title": "Q15. 利害が対立しないが納得度が低い",
                    "content": [
                        "全員が「反対ではない」が、誰も納得していない決定がある。PMとして、この状態をどう扱うか。",
                        "",
                        "意図:",
                        "表面合意と内的納得の違いを見抜けるか。"
                    ]
                },
                {
                    "section": "6. 権限・委譲",
                    "id": "Q16",
                    "title": "Q16. 自分の判断ミスに気づいたとき",
                    "content": [
                        "過去のPM判断が、現在の問題の原因になっていると分かった。この事実をどう扱い、どう修正するか。",
                        "",
                        "意図:",
                        "自己正当化をせず判断を更新できるか。"
                    ]
                },
                {
                    "section": "6. 権限・委譲",
                    "id": "Q17",
                    "title": "Q17. 判断を委譲するかどうか",
                    "content": [
                        "PMが判断すべき領域と、チームに委ねるべき領域の境界はどこか。その境界は状況によってどう変わるか。",
                        "",
                        "意図:",
                        "権限設計と責任設計の理解。"
                    ]
                }
            ],
            "7. 学習・適応": [
                {
                    "section": "7. 学習・適応",
                    "id": "Q18",
                    "title": "Q18. 成功パターンの再利用",
                    "content": [
                        "過去に成功した進め方を、別プロジェクトに適用しようとしている。どの条件が一致していれば再利用し、どこが違えば捨てるか。",
                        "",
                        "意図:",
                        "成功体験を抽象化しすぎない力。"
                    ]
                },
                {
                    "section": "7. 学習・適応",
                    "id": "Q19",
                    "title": "Q19. 優先順位が頻繁に変わる状況",
                    "content": [
                        "外部要因により優先順位が短期間で何度も変わる。PMとして、何を固定し、何を流動的に扱うか。",
                        "",
                        "意図:",
                        "不安定な状況での軸の持ち方。"
                    ]
                },
                {
                    "section": "7. 学習・適応",
                    "id": "Q20",
                    "title": "Q20. PMが不要になったと感じる瞬間",
                    "content": [
                        "プロジェクトが自走し始め、PMの介在が減っている。この状態を成功と見るか、リスクと見るか。",
                        "",
                        "意図:",
                        "PMの価値を自己中心的に定義していないか。"
                    ]
                }
            ]
        };

// ───── 品質・プロセス問題集データ（main.js から byte-equivalent 抽出）─────
export const qualityQuizData = {
            "1. 品質の兆候・評価": [
                {
                    "section": "1. 品質の兆候・評価",
                    "id": "Q1",
                    "title": "Q1. 品質が落ち始めた兆候",
                    "content": [
                        "あるプロジェクトで、リリース頻度は維持されているが軽微な不具合報告が徐々に増えている。この時点で、PMとして最初に確認すべき情報は何か。また、すぐに対策を打たない判断は成立するか。",
                        "",
                        "意図:",
                        "品質を「数値」ではなく変化の傾向で捉えられるか。"
                    ]
                },
                {
                    "section": "1. 品質の兆候・評価",
                    "id": "Q4",
                    "title": "Q4. 品質指標の選び方",
                    "content": [
                        "品質を可視化するため、KPIを設定することになった。不具合件数・テストカバレッジ・レビュー指摘数などが候補にある。どの指標を採用し、どれを採用しないか。その理由は。",
                        "",
                        "意図:",
                        "測れるもの＝見るべきものと誤解していないか。"
                    ]
                },
                {
                    "section": "1. 品質の兆候・評価",
                    "id": "Q10",
                    "title": "Q10. 「十分な品質」の定義",
                    "content": [
                        "プロジェクト終盤で「品質は十分か？」という問いが出た。この問いに対して、PMはどのように答えるべきか。また、「十分」という言葉をどう扱うか。",
                        "",
                        "意図:",
                        "品質を絶対値ではなく合意形成として扱えるか。"
                    ]
                },
                {
                    "section": "1. 品質の兆候・評価",
                    "id": "Q20",
                    "title": "Q20. 品質が良すぎると感じたとき",
                    "content": [
                        "品質指標は非常に良好だが、それに見合う価値が出ていないと感じる。この状態をどう評価するか。",
                        "",
                        "意図:",
                        "品質を目的化していないかの確認。"
                    ]
                }
            ],
            "2. テスト・検証": [
                {
                    "section": "2. テスト・検証",
                    "id": "Q2",
                    "title": "Q2. テスト工数削減の提案",
                    "content": [
                        "スケジュール遅延を理由に、開発側から「今回はテストケースを半分にしたい」という提案が出た。この提案を判断する際、PMは何を条件に可否を決めるべきか。",
                        "",
                        "意図:",
                        "品質を「削る／守る」の二択で考えていないか。"
                    ]
                },
                {
                    "section": "2. テスト・検証",
                    "id": "Q12",
                    "title": "Q12. テストが信頼されていない",
                    "content": [
                        "テストは実施されているが、「どうせ抜ける」という空気がある。品質を上げるために、まず何を変えるか。",
                        "",
                        "意図:",
                        "工数ではなく信頼の問題と認識できるか。"
                    ]
                }
            ],
            "3. 責任・原因分析": [
                {
                    "section": "3. 責任・原因分析",
                    "id": "Q3",
                    "title": "Q3. 品質問題の責任所在",
                    "content": [
                        "リリース後に不具合が発生し、開発チーム内で責任の押し付け合いが起きている。PMとして、原因分析と再発防止をどう切り分けるか。",
                        "",
                        "意図:",
                        "犯人探しと品質改善を分離できるか。"
                    ]
                },
                {
                    "section": "3. 責任・原因分析",
                    "id": "Q9",
                    "title": "Q9. 外部要因による品質低下",
                    "content": [
                        "外部APIや他チームの成果物が不安定で、自チームの品質が引きずられている。PMとして、どこまでを「自分たちの品質」として扱うか。",
                        "",
                        "意図:",
                        "品質の責任境界を定義できるか。"
                    ]
                },
                {
                    "section": "3. 責任・原因分析",
                    "id": "Q19",
                    "title": "Q19. 外部要因による品質低下（制御不能領域）",
                    "content": [
                        "外部APIや他チームの影響で品質問題が起きている。自チームで制御できない要因をどう扱うか。",
                        "",
                        "意図:",
                        "コントロール不能領域の設計的扱い。"
                    ]
                }
            ],
            "4. 技術的負債": [
                {
                    "section": "4. 技術的負債",
                    "id": "Q5",
                    "title": "Q5. 技術的負債の扱い",
                    "content": [
                        "明確な技術的負債が存在するが、短期的なビジネス要求が強く、返済の時間が取れない。PMとして、どのタイミングで「返す」と判断するか。",
                        "",
                        "意図:",
                        "技術的負債を感情論ではなく投資判断で扱えるか。"
                    ]
                }
            ],
            "5. プロセス": [
                {
                    "section": "5. プロセス",
                    "id": "Q6",
                    "title": "Q6. プロセスが形骸化したとき",
                    "content": [
                        "レビュー・朝会・ふりかえりは実施されているが、形だけになり、改善につながっていない。プロセスを増やさずに改善するなら、何を変えるか。",
                        "",
                        "意図:",
                        "プロセスを「足す人」か「意味を問い直す人」か。"
                    ]
                },
                {
                    "section": "5. プロセス",
                    "id": "Q14",
                    "title": "Q14. プロセスを守る人と破る人",
                    "content": [
                        "ルールを厳密に守る人と、柔軟に破る人が混在している。どちらを是とするか。",
                        "",
                        "意図:",
                        "プロセスを目的ではなく制約として扱えるか。"
                    ]
                },
                {
                    "section": "5. プロセス",
                    "id": "Q18",
                    "title": "Q18. プロセスが増えすぎたとき",
                    "content": [
                        "品質を守るためにプロセスが増え、現場の負担が明確に増している。どの基準で削るか。",
                        "",
                        "意図:",
                        "プロセスを削る判断ができるか。"
                    ]
                }
            ],
            "6. トレードオフ": [
                {
                    "section": "6. トレードオフ",
                    "id": "Q7",
                    "title": "Q7. 品質とスピードのトレードオフ",
                    "content": [
                        "重要顧客向けの機能リリースが迫っているが、現状の品質ではリスクが高いと判断される。リリース延期以外に、PMが取り得る選択肢は何か。",
                        "",
                        "意図:",
                        "トレードオフを多段階で考えられるか。"
                    ]
                },
                {
                    "section": "6. トレードオフ",
                    "id": "Q13",
                    "title": "Q13. 品質改善がスピードを落とすとき",
                    "content": [
                        "品質向上施策により、明確にスピードが落ち始めた。この状態をどう判断し、どう調整するか。",
                        "",
                        "意図:",
                        "品質とスピードを対立概念にしない。"
                    ]
                }
            ],
            "7. 属人化・構造": [
                {
                    "section": "7. 属人化・構造",
                    "id": "Q8",
                    "title": "Q8. 属人化と品質",
                    "content": [
                        "特定メンバーが抜けると、品質が急激に落ちる構造になっている。この問題を品質の問題として扱うか、プロセスの問題として扱うか。また、最初の一手は何か。",
                        "",
                        "意図:",
                        "人の問題を構造の問題に変換できるか。"
                    ]
                },
                {
                    "section": "7. 属人化・構造",
                    "id": "Q15",
                    "title": "Q15. レビューが属人化している",
                    "content": [
                        "特定の人のレビューだけが品質を担保している。この状態をどう評価し、どう是正するか。",
                        "",
                        "意図:",
                        "ヒーロー依存を構造の問題として見られるか。"
                    ]
                }
            ],
            "8. 文化・空気": [
                {
                    "section": "8. 文化・空気",
                    "id": "Q11",
                    "title": "Q11. 不具合が「慣れ」始めたとき",
                    "content": [
                        "軽微な不具合が常態化し、誰も強く問題視しなくなっている。PMとして、この状態をどう評価し、どう介入するか。",
                        "",
                        "意図:",
                        "劣化を文化として捉えられるか。"
                    ]
                }
            ],
            "9. 改善・学習": [
                {
                    "section": "9. 改善・学習",
                    "id": "Q16",
                    "title": "Q16. 再発防止が形だけになったとき",
                    "content": [
                        "再発防止策は毎回書かれているが、効果が見えない。どこに問題があると考えるか。",
                        "",
                        "意図:",
                        "再発防止を手続きではなく学習として扱えるか。"
                    ]
                },
                {
                    "section": "9. 改善・学習",
                    "id": "Q17",
                    "title": "Q17. 品質改善の効果が見えない",
                    "content": [
                        "改善施策を打っているが、良くなっている実感も悪化している実感もない。この状態をどう判断するか。",
                        "",
                        "意図:",
                        "改善を可視化できないリスクの理解。"
                    ]
                }
            ]
        };

// ───── v29 意思決定問題集データ（main.js から byte-equivalent 抽出）─────
export const architectureQuizData = {
            "第1章：アーキテクチャと境界の防衛戦": [
                {
                    id: "Q1",
                    title: "組織拡大と「バズワード」の誘惑",
                    situation: [
                        "現在、エンジニア10名体制で運用中のモノリシックなシステムがある。今後の事業拡大（半年以内にエンジニア50名体制への急拡大）を見越し、外部から招かれた新任CTOと、意識の高い若手テックリードがアーキテクチャの全面刷新を提案してきた。",
                        "彼らの主張は、「ドメインが未確定な現状であっても、将来の拡張性と各開発チームの自律性を担保するため、最初から完全なマイクロサービスアーキテクチャを採用すべきだ」というものだ。",
                        "さらに、「各サービスごとにリポジトリを完全に分割（Polyrepo化）し、コンテナオーケストレーションにはKubernetesを、サービス間通信の制御にはIstio（Service Mesh）を全面導入する」というロードマップを描いている。"
                    ],
                    stakeholders: [
                        { name: "CTO", quote: "最新のクラウドネイティブ・スタック（K8s、Istio）でエンジニアの採用力（技術広報）を爆発的に高めたい。GAFAもこの構成だ。" },
                        { name: "若手テックリード", quote: "各チームが他チームに依存せず、独立して好きな技術でデプロイできる究極の理想形です。CI/CDもサービスごとに最適化できます。" },
                        { name: "PM", quote: "で、これをやったら機能開発のスピードとベロシティは明日から2倍になるんだよね？" }
                    ],
                    question: "コンウェイの法則、ネットワークの8つの誤謬、そして分散モノリス化の恐怖を考慮し、この提案に対するあなたの意思決定を下せ。"
                }
            ],
            "第2章：データストアとトランザクションの泥沼": [
                {
                    id: "Q2",
                    title: "「技術の多様性（Polyglot Persistence）」と分散トランザクションの罠",
                    situation: [
                        "新規の重要サブシステム（決済・ポイント管理を含む）の開発において、要件として「スキーマが頻繁に変わる非定型データの保存」と「他システムと連携するための非同期ジョブキュー」が追加された。",
                        "現在、システムのメインDBは堅牢にチューニングされた単一のPostgreSQLである。",
                        "しかし、アプリケーション開発チームが「それぞれの用途に最適な技術を選ぶべきだ（Polyglot Persistence）」と主張し、「ドキュメント指向DBとしてMongoDBを、メッセージブローカーとしてApache Kafkaを新規導入する」という構成案を持ってきた。",
                        "さらに、複数サービスにまたがるデータ整合性を担保するため、非同期の「Sagaパターン（補償トランザクション）」を自前で実装する計画を立てている。"
                    ],
                    stakeholders: [
                        { name: "アプリエンジニア", quote: "RDBの厳格なスキーマ変更（マイグレーション）待ちで開発がブロックされるのは嫌だ。MongoDBならスキーマレスで最高だ。Kafkaなら毎秒数万件のイベントでもスケールする。" },
                        { name: "ITコンサル", quote: "適材適所の技術選定こそがモダンです。マイクロサービス間の結果整合性（Eventual Consistency）はSagaパターンで解決できます。" }
                    ],
                    question: "ミドルウェアの増加がもたらす運用負荷（パッチ当て、バックアップ、監視、障害切り分けの複雑化）と、Sagaパターンのデバッグ難易度を念頭に置き、あなたの意思決定を下せ。"
                }
            ],
            "第3章：APIとリアルタイム通信の妥協点": [
                {
                    id: "Q3",
                    title: "過剰なリアルタイム性と「ステートフル」なインフラの恐怖",
                    situation: [
                        "新機能として「ユーザー向けダッシュボードの通知・数値のリアルタイム更新」が求められた。",
                        "フロントエンドチームが「画面のチラつきを完全に無くし、極上のUXを提供するため、完全な双方向通信であるWebSocketを全面導入したい」と息巻いている。",
                        "さらに、「クライアント側が欲しいデータだけを柔軟に取得できるよう、GraphQLを用いたBFF（Backends For Frontends）層をNode.jsで新規構築する」と提案してきた。"
                    ],
                    stakeholders: [
                        { name: "フロントエンドTL", quote: "REST APIのオーバーフェッチ/アンダーフェッチにはもうウンザリだ。WebSocketでサーバーからバンバン状態をプッシュしたい。" },
                        { name: "バックエンドエンジニア", quote: "WebSocketのコネクション維持でメモリがどれだけ食われるか分かってるのか？スケールアウト時のPub/Sub同期（Redis等）の構築はどうするんだ？" }
                    ],
                    question: "ステートフルなコネクションがもたらすローリングアップデートの困難さ、ロードバランサーのタイムアウト問題、Thundering Herd（再接続の嵐）のリスク、そしてREST API（CDNキャッシュ）の恩恵を手放すことの重大さを考慮し、あなたの意思決定を下せ。"
                }
            ],
            "第4章：可用性とFinOps（コスト）の天秤": [
                {
                    id: "Q4",
                    title: "「絶対に止まらないシステム」という幻とオーバーエンジニアリング",
                    situation: [
                        "事業部門トップが「今回の新サービスは会社の命運を握っている。絶対に止まってはならない。SLA 99.99%（年間ダウンタイム52分以内）を絶対保証しろ」と要求してきた。",
                        "これを受け、外部インテグレーションベンダーが「AWSの東京リージョンと大阪リージョンを用いたマルチリージョン・Active-Active構成」という重厚長大なインフラ設計案を提出した。",
                        "さらに「監視にはフル機能のDatadogを全レイヤー（APM、Log, Infrastructure）に導入する（試算ではDatadogの利用料がAWSのインフラコストを上回る）」と息巻いている。"
                    ],
                    stakeholders: [
                        { name: "事業部長", quote: "障害でサービスが止まったら日経新聞沙汰だ。インフラ投資に金に糸目はつけない！（※稼働半年後には確実にインフラコスト半減のプレッシャーをかけてくる）" },
                        { name: "ベンダーアーキテクト", quote: "CAP定理を乗り越える最高峰のエンタープライズ構成です。リージョン障害が起きても無停止でルーティングされます。" }
                    ],
                    question: "Active-Active構成がもたらすデータ同期（Split-brain）の地獄、莫大なEgress（データ転送）料金、そして「MTBF（平均故障間隔）の最大化」という幻想ではなく、「MTTR（平均修復時間）の極小化」こそが真の可用性であるというSREの原則に基づき、あなたの意思決定を下せ。"
                }
            ],
            "第5章：技術的負債とインシデント対応の狂気": [
                {
                    id: "Q5",
                    title: "P1障害対応中のリファクタリング衝動と、Git Force Pushの惨劇",
                    situation: [
                        "金曜日の深夜2時。本番環境で決済処理が全停止するP1（最高優先度）インシデントが発生した。",
                        "原因究明のため緊急招集された開発メンバーがパニックに陥っている。",
                        "一人のシニアエンジニアが「原因は決済モジュールのクラス設計がクソだからだ！今からデザインパターンを適用して根本的にリファクタリングする！」と叫び、数千行のコードを書き換え始めた。",
                        "同時に、別の若手エンジニアが「バグが混入したコミットを見つけました！メインブランチをGit Force Pushして、昨日の状態に強制的に巻き戻します！」とコマンドを実行しようとしている。"
                    ],
                    stakeholders: [
                        { name: "シニアエンジニア", quote: "どうせ直すなら、技術的負債も一緒に返済すべきだ！これが根本対応だ！" },
                        { name: "若手エンジニア", quote: "Force Pushすれば一瞬でバグる前に戻せます！早く復旧させないと！" },
                        { name: "カスタマーサポート", quote: "お客様からのクレーム電話が鳴り止みません！いつ復旧するんですか！？" }
                    ],
                    question: "インシデント中の「Mitigation（影響緩和）」と「Resolution（根本解決）」の混同が引き起こす二次災害、そして本番ブランチへの強制上書きによる状態の不整合（DBスキーマとの乖離など）の恐怖を制圧し、現場指揮官としてのあなたの意思決定を下せ。"
                }
            ],
            "第6章：アジャイルの闇と条件分岐の地獄": [
                {
                    id: "Q6",
                    title: "放置されたFeature Flags（Dead Flags）の清算",
                    situation: [
                        "トランクベース開発（Trunk-based Development）を推進するため、機能のオン/オフを動的に切り替える「Feature Flags（機能フラグ）」システムを導入して1年が経過した。",
                        "アジャイルなデプロイは実現したが、深刻な問題が発覚した。リリース済みの古い機能フラグのクリーンアップが一切行われておらず、ソースコードの至る所に「数千個の不要なIF文（Dead Flags）」が散乱している状態だ。",
                        "テストコードの組み合わせ（Cyclomatic Complexity）は天文学的な数字に爆発し、誰も全体像を把握できず、昨日ついに「古いフラグの誤操作による意図しない旧画面の露出」という本番障害が発生した。"
                    ],
                    stakeholders: [
                        { name: "プロダクトオーナー", quote: "コードの掃除（リファクタリング）にスプリントのポイントを割く余裕はない。新機能（新しいフラグ）の開発を止めないでくれ。" },
                        { name: "開発チーム", quote: "どのフラグが今本番でTrueになってるか、もう誰も分かりません。消すのが怖くて触れません。" }
                    ],
                    question: "技術的負債が限界を超え、システムの予測可能性が完全に崩壊する一歩手前にある。運用上の安全性とコードの健全性を取り戻すための、あなたの意思決定を下せ。"
                }
            ]
        };

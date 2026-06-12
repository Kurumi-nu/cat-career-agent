DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS events;

CREATE TABLE places (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  area TEXT NOT NULL,
  tag TEXT NOT NULL,
  rating REAL NOT NULL,
  description TEXT NOT NULL,
  best_time TEXT NOT NULL,
  access TEXT NOT NULL,
  image TEXT NOT NULL DEFAULT ''
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  season TEXT NOT NULL,
  date_label TEXT NOT NULL,
  description TEXT NOT NULL
);

INSERT INTO places (name, category, area, tag, rating, description, best_time, access, image) VALUES
('ランタン運河', '名所', '旧市街', '夕暮れ', 4.9, '街の中心を流れる全長4.2kmの運河。橋ごとに灯るランタンが水面に映り、ミラノアらしい夜景を作ります。', '夕暮れ以降', '中央桟橋から徒歩4分', '/images/spots/lantern-canal.png'),
('風見の観測塔', '名所', '丘陵区', '展望', 4.7, '旧港、新市街、内海を一望できる高さ86mの展望塔。屋上の風見盤は街の象徴です。', '20:00前後', '水上トラムT2線 終点', '/images/spots/observatory-tower.png'),
('北桟橋市場', '食', '北桟橋', '朝市', 4.6, '魚介、柑橘、焼き菓子が並ぶ朝市。旅人には焼きレモンのパンと港のスープが人気です。', '6:00-9:00', '中央駅から徒歩12分', '/images/spots/north-pier-market.png'),
('硝子屋根の回廊', '建築', '旧市街', '雨の日', 4.5, '商店街と美術館をつなぐ透明な屋根の歩道。雨の日は石畳に光がやわらかく落ちます。', '午後', '市庁舎前から徒歩2分', '/images/spots/glass-arcade.png'),
('潮風植物園', '自然', '南岸', '散策', 4.3, '海辺の植物だけを集めた庭園。午前中は香りが濃く、静かな散策に向いています。', '午前中', '電気バスB4線 植物園前', '/images/spots/botanical-garden.png'),
('月波温浴場', '体験', '南岸', '夜', 4.4, '観光後に立ち寄れる公共浴場。丸窓から運河の灯りが見える浴室が名物です。', '21:00以降', '水上トラムT1線 月波前', '/images/spots/moonwave-bath.png'),
('回廊美術館', '文化', '美術区', '屋内', 4.2, 'ガラス回廊の途中にある小さな美術館。港町の設計図や古い航海日誌も展示されています。', '雨の日', '硝子屋根の回廊内', '/images/spots/arcade-museum.png'),
('灯台広場', '名所', '旧港', '夜市', 4.8, '毎月17日に夜市が開かれる広場。小皿料理の屋台と手仕事の露店が22時まで並びます。', '毎月17日', '中央桟橋から徒歩7分', '/images/spots/lighthouse-square.png');

INSERT INTO events (name, season, date_label, description) VALUES
('水鏡の花舟', '春', '4月上旬', '春の花を積んだ小舟が旧市街をゆっくり巡る季節行事です。'),
('海風映画祭', '夏', '8月最終週', '港の倉庫壁をスクリーンにした屋外上映会。夜風が気持ちよい時期に開催されます。'),
('ランタン点灯週間', '秋', '11月中旬', '橋、窓辺、船着場に手作りランタンが灯る、ミラノアで最も人気のある一週間です。'),
('回廊の夜市', '毎月', '毎月17日', '灯台広場に小皿料理と工芸品の店が並ぶ月例マーケットです。');

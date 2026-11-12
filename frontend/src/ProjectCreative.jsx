import {useState} from 'react';
import {ArrowUpRight} from 'lucide-react';

// Each direction is chosen for the actual brand, not the position of its card.
export const creativeDirections = {
  'svvad-pro': {bg:'#f1eee4',ink:'#23392a',accent:'#ed6a25',title:['Good food.','Great energy.'],label:'Food & nutrition',style:'orbit'},
  oatful: {bg:'#e8edbc',ink:'#244c38',accent:'#ec8359',title:['A little oat.','A lot of joy.'],label:'The everyday pantry',style:'play'},
  iiebm: {bg:'#e3eaf0',ink:'#123760',accent:'#d8b24b',title:['An ambitious','next chapter.'],label:'Education & opportunity',style:'architect'},
  indewheelers: {bg:'#172021',ink:'#fff7e8',accent:'#eb5b34',title:['Built for','the fast lane.'],label:'Motorsport & performance',style:'speed'},
  shreekrupa: {bg:'#e8e9e6',ink:'#282c2e',accent:'#d32c27',title:['Precision.','In every detail.'],label:'Industrial automation',style:'architect'},
  manore: {bg:'#dbe1e1',ink:'#12314b',accent:'#7a9daf',title:['A considered','daily ritual.'],label:'Skincare & self care',style:'minimal'},
  shrisiddh: {bg:'#dce4cd',ink:'#234a34',accent:'#b48a35',title:['Rooted in','something real.'],label:'Ayurvedic wellness',style:'botanical'},
  sudhamrutam: {bg:'#f0dec1',ink:'#60261f',accent:'#b48a38',title:['Nature, in','everyday life.'],label:'Herbal wellness',style:'botanical'},
  'red-dot-media': {bg:'#eeeae5',ink:'#242325',accent:'#de2333',title:['Make a mark.','Leave a feeling.'],label:'A creative agency',style:'studio'},
  'salgar-tea': {bg:'#efc95c',ink:'#6d241e',accent:'#c63831',title:['Good things','start with chai.'],label:'Tea & togetherness',style:'editorial',portrait:true},
  thrillax: {bg:'#c9e9ec',ink:'#154a56',accent:'#eaa840',title:['A little escape.','A big adventure.'],label:'Water, adventure & play',style:'orbit'},
  makhanawala: {bg:'#f1c84d',ink:'#572a21',accent:'#ae342d',title:['Small bites.','Big character.'],label:'Snacks & savouries',style:'editorial',portrait:true},
  'urban-monk': {bg:'#f0b493',ink:'#4c3022',accent:'#c0cc4a',title:['Fresh fizz.','Urban spirit.'],label:'Beverages & refreshment',style:'editorial',portrait:true},
  daishik: {bg:'#e8e1bd',ink:'#285035',accent:'#b84b32',title:['Instant flavour.','Lasting delight.'],label:'Chutneys & Indian snacks',style:'play',brandAsset:true},
  dealishaa: {bg:'#f8e5cd',ink:'#7e3325',accent:'#b78034',title:['Flavour,','beautifully simple.'],label:'Food & ingredients',style:'editorial',portrait:true},
  lavenizzo: {bg:'#e5e3d3',ink:'#33442a',accent:'#912e43',title:['A taste of','the exceptional.'],label:'Wine & craftsmanship',style:'editorial',portrait:true},
  'janaki-sadan': {bg:'#eee0c8',ink:'#6b3e24',accent:'#aa8129',title:['A sense','of place.'],label:'A distinctive brand presence',style:'editorial',portrait:true},
  'govind-milk': {bg:'#e3edf2',ink:'#114b85',accent:'#7cac4d',title:['A fresh','perspective.'],label:'Milk & dairy',style:'orbit'},
  'purely-desi': {bg:'#e9dfc8',ink:'#543f21',accent:'#b08c41',title:['Pure roots.','Modern living.'],label:'Honey & traditional essentials',style:'botanical'},
  'nutrico-delight': {bg:'#f2d45c',ink:'#244c60',accent:'#d65176',title:['Full of flavour.','Full of life.'],label:'Flavoured drinks',style:'play'},
  'pillar-stone': {bg:'#dcdedb',ink:'#253747',accent:'#9a8866',title:['Places with','possibility.'],label:'Property & communities',style:'architect'},
  'wwc-crm': {bg:'#e4dcf2',ink:'#392c54',accent:'#9170bf',title:['Less friction.','More flow.'],label:'Internal workflow application',style:'studio'}
};

const asset = path => path?.startsWith('/') || /^https?:\/\//.test(path || '') ? path : import.meta.env.BASE_URL + (path || '');

export default function ProjectCreative({project,crm}) {
  const [failed,setFailed] = useState(false);
  const d = creativeDirections[project.slug] || {bg:project.color || '#e5dfef',ink:'#302c36',accent:'#9c7aba',title:[project.title],label:project.category,style:'minimal'};
  const image = project.image;
  return <div className={`portfolio-cover cover-${d.style} ${d.portrait ? 'cover-portrait' : ''}`} style={{'--cover-bg':d.bg,'--cover-ink':d.ink,'--cover-accent':d.accent}}>
    <div className="cover-motif" aria-hidden="true"><i/><i/><i/></div>
    <div className="cover-top"><span>{d.label}</span><span className="cover-mark" aria-hidden="true">↗</span></div>
    <div className="cover-heading" aria-hidden="true">{d.title.map(line=><span key={line}>{line}</span>)}</div>
    <div className="cover-media">
      {crm || (image && !failed ? <>
        {!d.portrait && !d.brandAsset && <div className="cover-browser" aria-hidden="true"><span>● ● ●</span><small>{project.url ? new URL(project.url).hostname.replace(/^www\./,'') : project.title}</small><span>↗</span></div>}
        <img key={image} src={asset(image)} alt={`${project.title} — ${d.portrait || d.brandAsset ? 'brand visual' : 'website preview'}`} loading="lazy" decoding="async" onError={()=>setFailed(true)}/>
      </> : <div className="cover-placeholder"><strong>{project.title}</strong><span>{project.category}</span></div>)}
    </div>
    <div className="cover-bottom"><span>{project.title}</span><ArrowUpRight aria-hidden="true"/></div>
  </div>;
}

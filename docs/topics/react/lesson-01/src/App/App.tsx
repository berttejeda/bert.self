import React,{useEffect,useState} from 'react';
import Cookies from 'universal-cookie';

// Main style
import '../index.scss'

const cookies = new Cookies();

if (window.performance) {
  if (performance.navigation.type == 1) {
    console.log( "Application restarted" );
  } else {
    console.log( "Application start" );
  }
}

export default function App () {



const openInNewTab = url => {
    cookies.set('auth_token', '123456', { path: '/', maxAge: 5 });
    cookies.set('endpoint_address', 'https://vcenter.local', { path: '/', maxAge: 5 });
    cookies.set('targe_port', '10270', { path: '/', maxAge: 5 });
    console.log(cookies.get('auth_token')); // 123456
    window.open(url, '_blank', 'noopener,noreferrer');
  };


  return (
  <div>
    <button onClick={() => openInNewTab('http://localhost:9001')}>
      Connect to Endpoint
    </button>
  </div>


  );

}
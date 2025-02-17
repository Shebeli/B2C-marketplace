export function Footer() {
  const iconWidth = 60;
  const iconHeight = 60;
  return (
    <footer className="footer footer-center bg-base-200 text-base-content rounded p-10 border-t-2">
      <nav className="grid grid-flow-col gap-4">
        <a className="link link-hover">درباره ما</a>
        <a className="link link-hover">تماس با ما</a>
      </nav>
      <nav>
        <p className="text-lg">ابزار استفاده شده برای توسعه اپلیکیشن:</p>
        <div className="grid grid-flow-col gap-6 mt-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width={iconWidth}
            height={iconHeight}
            viewBox="0 0 128 128"
          >
            <path
              fill="#38bdf8"
              d="M64.004 25.602c-17.067 0-27.73 8.53-32 25.597c6.398-8.531 13.867-11.73 22.398-9.597c4.871 1.214 8.352 4.746 12.207 8.66C72.883 56.629 80.145 64 96.004 64c17.066 0 27.73-8.531 32-25.602c-6.399 8.536-13.867 11.735-22.399 9.602c-4.87-1.215-8.347-4.746-12.207-8.66c-6.27-6.367-13.53-13.738-29.394-13.738zM32.004 64c-17.066 0-27.73 8.531-32 25.602C6.402 81.066 13.87 77.867 22.402 80c4.871 1.215 8.352 4.746 12.207 8.66c6.274 6.367 13.536 13.738 29.395 13.738c17.066 0 27.73-8.53 32-25.597c-6.399 8.531-13.867 11.73-22.399 9.597c-4.87-1.214-8.347-4.746-12.207-8.66C55.128 71.371 47.868 64 32.004 64zm0 0"
            />
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width={iconWidth}
            height={iconHeight}
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M2.64 10.655v-1.6h1.31v4.92H2.64v-.31c-.09.09-.2.16-.32.22c-.18.09-.39.13-.62.13c-.34 0-.63-.08-.89-.24s-.46-.38-.6-.67c-.14-.28-.21-.61-.21-.98s.07-.68.21-.96c.14-.28.34-.5.59-.65c.25-.15.55-.23.88-.23c.23 0 .45.05.64.14c.12.06.23.13.33.22l-.01.01Zm-.66 2.3c.2 0 .35-.07.47-.21c.12-.14.18-.33.18-.57s-.06-.43-.18-.57c-.12-.14-.28-.21-.47-.21s-.35.07-.48.21c-.12.14-.19.33-.19.57s.06.42.19.57a.6.6 0 0 0 .48.21Zm4.57-1.23c0-.12-.05-.21-.14-.27c-.1-.08-.24-.12-.44-.12c-.14 0-.29.02-.47.07s-.35.11-.53.2l-.08.04l-.38-.93l.07-.03c.29-.13.56-.23.83-.29c.26-.06.54-.1.82-.1c.5 0 .89.12 1.17.35c.28.24.43.57.43.99v2.34H6.54v-.26c-.24.21-.56.31-.96.31s-.7-.11-.93-.32c-.23-.22-.34-.5-.34-.85s.13-.63.37-.83s.59-.3 1.04-.3h.83Zm0 .98v-.2h-.59c-.28 0-.39.09-.39.27c0 .09.03.17.09.22c.07.06.16.09.29.09c.15 0 .29-.04.4-.11s.17-.16.2-.26v-.01Zm2.53-2.58a.663.663 0 0 1-.68-.69c0-.19.06-.37.19-.5s.3-.19.49-.19s.36.07.49.19c.13.13.19.3.19.5s-.06.36-.19.49s-.3.2-.49.2Zm.66.21v3.63h-1.3v-3.63h1.3Zm2.01 3.68c-.3 0-.59-.04-.87-.13s-.53-.21-.74-.38l-.05-.04l.43-.89l.08.06c.19.13.39.23.6.31c.21.07.4.11.58.11c.1 0 .17-.02.22-.04c.04-.02.05-.05.05-.08c0-.05-.03-.09-.1-.12c-.09-.04-.24-.09-.44-.15c-.25-.07-.45-.15-.61-.22c-.17-.08-.32-.19-.44-.34a.932.932 0 0 1-.2-.61c0-.38.14-.68.43-.89s.64-.31 1.08-.31c.26 0 .52.04.77.11s.49.17.72.31l.07.04l-.46.89l-.08-.04c-.44-.23-.79-.34-1.06-.34c-.08 0-.15 0-.19.04c-.03.02-.05.05-.05.09s.03.08.09.11c.09.04.23.09.43.15c.25.07.46.15.63.22c.18.08.33.19.46.34c.13.16.2.37.2.61c0 .38-.15.68-.44.89s-.66.31-1.11.31v-.01Zm3.2-.23l-1.47-3.46h1.36l.76 2.08l.68-2.08h1.32l-.05.12l-1.49 3.8c-.14.34-.32.59-.56.76c-.24.17-.53.25-.87.25c-.2 0-.39-.03-.57-.09c-.18-.06-.35-.16-.51-.29l-.06-.05l.56-.94l.08.06c.07.06.14.11.21.13c.06.03.13.04.2.04c.16 0 .26-.07.34-.22l.06-.12h.01v.01Zm5.14.27c-.42 0-.8-.08-1.12-.25c-.32-.17-.58-.4-.75-.71c-.18-.31-.26-.66-.26-1.06v-2.72h1.34v2.72c0 .26.08.46.23.62c.15.15.34.23.57.23s.41-.07.55-.23c.14-.15.21-.36.21-.62v-2.72h1.34v2.72c0 .4-.09.76-.26 1.06c-.17.31-.42.54-.74.71c-.32.16-.69.25-1.11.25Zm3.91-.08h-1.34v-4.66H24v4.66Z"
            />
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width={iconWidth}
            height={iconHeight}
            viewBox="0 0 128 128"
          >
            <path fill="#fff" d="M22.67 47h99.67v73.67H22.67z" />
            <path
              fill="#007acc"
              d="M1.5 63.91v62.5h125v-125H1.5zm100.73-5a15.56 15.56 0 0 1 7.82 4.5a20.58 20.58 0 0 1 3 4c0 .16-5.4 3.81-8.69 5.85c-.12.08-.6-.44-1.13-1.23a7.09 7.09 0 0 0-5.87-3.53c-3.79-.26-6.23 1.73-6.21 5a4.58 4.58 0 0 0 .54 2.34c.83 1.73 2.38 2.76 7.24 4.86c8.95 3.85 12.78 6.39 15.16 10c2.66 4 3.25 10.46 1.45 15.24c-2 5.2-6.9 8.73-13.83 9.9a38.32 38.32 0 0 1-9.52-.1a23 23 0 0 1-12.72-6.63c-1.15-1.27-3.39-4.58-3.25-4.82a9.34 9.34 0 0 1 1.15-.73L82 101l3.59-2.08l.75 1.11a16.78 16.78 0 0 0 4.74 4.54c4 2.1 9.46 1.81 12.16-.62a5.43 5.43 0 0 0 .69-6.92c-1-1.39-3-2.56-8.59-5c-6.45-2.78-9.23-4.5-11.77-7.24a16.48 16.48 0 0 1-3.43-6.25a25 25 0 0 1-.22-8c1.33-6.23 6-10.58 12.82-11.87a31.66 31.66 0 0 1 9.49.26zm-29.34 5.24v5.12H56.66v46.23H45.15V69.26H28.88v-5a49.19 49.19 0 0 1 .12-5.17C29.08 59 39 59 51 59h21.83z"
            />
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            role="img"
            width={iconWidth}
            height={iconHeight}
            preserveAspectRatio="xMidYMid meet"
            viewBox="0 0 256 228"
          >
            <path
              fill="#00D8FF"
              d="M210.483 73.824a171.49 171.49 0 0 0-8.24-2.597c.465-1.9.893-3.777 1.273-5.621c6.238-30.281 2.16-54.676-11.769-62.708c-13.355-7.7-35.196.329-57.254 19.526a171.23 171.23 0 0 0-6.375 5.848a155.866 155.866 0 0 0-4.241-3.917C100.759 3.829 77.587-4.822 63.673 3.233C50.33 10.957 46.379 33.89 51.995 62.588a170.974 170.974 0 0 0 1.892 8.48c-3.28.932-6.445 1.924-9.474 2.98C17.309 83.498 0 98.307 0 113.668c0 15.865 18.582 31.778 46.812 41.427a145.52 145.52 0 0 0 6.921 2.165a167.467 167.467 0 0 0-2.01 9.138c-5.354 28.2-1.173 50.591 12.134 58.266c13.744 7.926 36.812-.22 59.273-19.855a145.567 145.567 0 0 0 5.342-4.923a168.064 168.064 0 0 0 6.92 6.314c21.758 18.722 43.246 26.282 56.54 18.586c13.731-7.949 18.194-32.003 12.4-61.268a145.016 145.016 0 0 0-1.535-6.842c1.62-.48 3.21-.974 4.76-1.488c29.348-9.723 48.443-25.443 48.443-41.52c0-15.417-17.868-30.326-45.517-39.844Zm-6.365 70.984c-1.4.463-2.836.91-4.3 1.345c-3.24-10.257-7.612-21.163-12.963-32.432c5.106-11 9.31-21.767 12.459-31.957c2.619.758 5.16 1.557 7.61 2.4c23.69 8.156 38.14 20.213 38.14 29.504c0 9.896-15.606 22.743-40.946 31.14Zm-10.514 20.834c2.562 12.94 2.927 24.64 1.23 33.787c-1.524 8.219-4.59 13.698-8.382 15.893c-8.067 4.67-25.32-1.4-43.927-17.412a156.726 156.726 0 0 1-6.437-5.87c7.214-7.889 14.423-17.06 21.459-27.246c12.376-1.098 24.068-2.894 34.671-5.345a134.17 134.17 0 0 1 1.386 6.193ZM87.276 214.515c-7.882 2.783-14.16 2.863-17.955.675c-8.075-4.657-11.432-22.636-6.853-46.752a156.923 156.923 0 0 1 1.869-8.499c10.486 2.32 22.093 3.988 34.498 4.994c7.084 9.967 14.501 19.128 21.976 27.15a134.668 134.668 0 0 1-4.877 4.492c-9.933 8.682-19.886 14.842-28.658 17.94ZM50.35 144.747c-12.483-4.267-22.792-9.812-29.858-15.863c-6.35-5.437-9.555-10.836-9.555-15.216c0-9.322 13.897-21.212 37.076-29.293c2.813-.98 5.757-1.905 8.812-2.773c3.204 10.42 7.406 21.315 12.477 32.332c-5.137 11.18-9.399 22.249-12.634 32.792a134.718 134.718 0 0 1-6.318-1.979Zm12.378-84.26c-4.811-24.587-1.616-43.134 6.425-47.789c8.564-4.958 27.502 2.111 47.463 19.835a144.318 144.318 0 0 1 3.841 3.545c-7.438 7.987-14.787 17.08-21.808 26.988c-12.04 1.116-23.565 2.908-34.161 5.309a160.342 160.342 0 0 1-1.76-7.887Zm110.427 27.268a347.8 347.8 0 0 0-7.785-12.803c8.168 1.033 15.994 2.404 23.343 4.08c-2.206 7.072-4.956 14.465-8.193 22.045a381.151 381.151 0 0 0-7.365-13.322Zm-45.032-43.861c5.044 5.465 10.096 11.566 15.065 18.186a322.04 322.04 0 0 0-30.257-.006c4.974-6.559 10.069-12.652 15.192-18.18ZM82.802 87.83a323.167 323.167 0 0 0-7.227 13.238c-3.184-7.553-5.909-14.98-8.134-22.152c7.304-1.634 15.093-2.97 23.209-3.984a321.524 321.524 0 0 0-7.848 12.897Zm8.081 65.352c-8.385-.936-16.291-2.203-23.593-3.793c2.26-7.3 5.045-14.885 8.298-22.6a321.187 321.187 0 0 0 7.257 13.246c2.594 4.48 5.28 8.868 8.038 13.147Zm37.542 31.03c-5.184-5.592-10.354-11.779-15.403-18.433c4.902.192 9.899.29 14.978.29c5.218 0 10.376-.117 15.453-.343c-4.985 6.774-10.018 12.97-15.028 18.486Zm52.198-57.817c3.422 7.8 6.306 15.345 8.596 22.52c-7.422 1.694-15.436 3.058-23.88 4.071a382.417 382.417 0 0 0 7.859-13.026a347.403 347.403 0 0 0 7.425-13.565Zm-16.898 8.101a358.557 358.557 0 0 1-12.281 19.815a329.4 329.4 0 0 1-23.444.823c-7.967 0-15.716-.248-23.178-.732a310.202 310.202 0 0 1-12.513-19.846h.001a307.41 307.41 0 0 1-10.923-20.627a310.278 310.278 0 0 1 10.89-20.637l-.001.001a307.318 307.318 0 0 1 12.413-19.761c7.613-.576 15.42-.876 23.31-.876H128c7.926 0 15.743.303 23.354.883a329.357 329.357 0 0 1 12.335 19.695a358.489 358.489 0 0 1 11.036 20.54a329.472 329.472 0 0 1-11 20.722Zm22.56-122.124c8.572 4.944 11.906 24.881 6.52 51.026c-.344 1.668-.73 3.367-1.15 5.09c-10.622-2.452-22.155-4.275-34.23-5.408c-7.034-10.017-14.323-19.124-21.64-27.008a160.789 160.789 0 0 1 5.888-5.4c18.9-16.447 36.564-22.941 44.612-18.3ZM128 90.808c12.625 0 22.86 10.235 22.86 22.86s-10.235 22.86-22.86 22.86s-22.86-10.235-22.86-22.86s10.235-22.86 22.86-22.86Z"
            ></path>
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width={iconWidth}
            height={iconHeight}
            viewBox="0 0 128 128"
          >
            <linearGradient
              id="deviconPython0"
              x1="70.252"
              x2="170.659"
              y1="1237.476"
              y2="1151.089"
              gradientTransform="matrix(.563 0 0 -.568 -29.215 707.817)"
              gradientUnits="userSpaceOnUse"
            >
              <stop offset="0" stop-color="#5A9FD4" />
              <stop offset="1" stop-color="#306998" />
            </linearGradient>
            <linearGradient
              id="deviconPython1"
              x1="209.474"
              x2="173.62"
              y1="1098.811"
              y2="1149.537"
              gradientTransform="matrix(.563 0 0 -.568 -29.215 707.817)"
              gradientUnits="userSpaceOnUse"
            >
              <stop offset="0" stop-color="#FFD43B" />
              <stop offset="1" stop-color="#FFE873" />
            </linearGradient>
            <path
              fill="url(#deviconPython0)"
              d="M63.391 1.988c-4.222.02-8.252.379-11.8 1.007c-10.45 1.846-12.346 5.71-12.346 12.837v9.411h24.693v3.137H29.977c-7.176 0-13.46 4.313-15.426 12.521c-2.268 9.405-2.368 15.275 0 25.096c1.755 7.311 5.947 12.519 13.124 12.519h8.491V67.234c0-8.151 7.051-15.34 15.426-15.34h24.665c6.866 0 12.346-5.654 12.346-12.548V15.833c0-6.693-5.646-11.72-12.346-12.837c-4.244-.706-8.645-1.027-12.866-1.008zM50.037 9.557c2.55 0 4.634 2.117 4.634 4.721c0 2.593-2.083 4.69-4.634 4.69c-2.56 0-4.633-2.097-4.633-4.69c-.001-2.604 2.073-4.721 4.633-4.721z"
              transform="translate(0 10.26)"
            />
            <path
              fill="url(#deviconPython1)"
              d="M91.682 28.38v10.966c0 8.5-7.208 15.655-15.426 15.655H51.591c-6.756 0-12.346 5.783-12.346 12.549v23.515c0 6.691 5.818 10.628 12.346 12.547c7.816 2.297 15.312 2.713 24.665 0c6.216-1.801 12.346-5.423 12.346-12.547v-9.412H63.938v-3.138h37.012c7.176 0 9.852-5.005 12.348-12.519c2.578-7.735 2.467-15.174 0-25.096c-1.774-7.145-5.161-12.521-12.348-12.521h-9.268zM77.809 87.927c2.561 0 4.634 2.097 4.634 4.692c0 2.602-2.074 4.719-4.634 4.719c-2.55 0-4.633-2.117-4.633-4.719c0-2.595 2.083-4.692 4.633-4.692z"
              transform="translate(0 10.26)"
            />
            <radialGradient
              id="deviconPython2"
              cx="1825.678"
              cy="444.45"
              r="26.743"
              gradientTransform="matrix(0 -.24 -1.055 0 532.979 557.576)"
              gradientUnits="userSpaceOnUse"
            >
              <stop offset="0" stop-color="#B8B8B8" stop-opacity=".498" />
              <stop offset="1" stop-color="#7F7F7F" stop-opacity="0" />
            </radialGradient>
            <path
              fill="url(#deviconPython2)"
              d="M97.309 119.597c0 3.543-14.816 6.416-33.091 6.416c-18.276 0-33.092-2.873-33.092-6.416c0-3.544 14.815-6.417 33.092-6.417c18.275 0 33.091 2.872 33.091 6.417z"
              opacity=".444"
            />
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width={iconWidth}
            height={iconHeight}
            viewBox="0 0 256 256"
          >
            <g fill="none">
              <rect width="256" height="256" fill="#092E20" rx="60" />
              <path
                fill="#fff"
                d="M112.689 51h28.615v132.45c-14.679 2.787-25.456 3.902-37.161 3.902C69.209 187.351 51 171.559 51 141.271c0-29.173 19.325-48.124 49.24-48.124c4.645 0 8.175.37 12.449 1.485V51Zm0 66.671c-3.344-1.113-6.131-1.485-9.661-1.485c-14.493 0-22.856 8.919-22.856 24.526c0 15.238 7.991 23.599 22.67 23.599c3.157 0 5.76-.186 9.847-.742v-45.898Z"
              />
              <path
                fill="#fff"
                d="M186.826 95.19v66.332c0 22.856-1.672 33.818-6.689 43.295c-4.646 9.106-10.778 14.865-23.413 21.183l-26.571-12.636c12.635-5.945 18.767-11.146 22.668-19.139c4.089-8.175 5.391-17.652 5.391-42.55V95.189h28.614Zm-28.614-44.038h28.614V80.51h-28.614V51.152Z"
              />
            </g>
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width={iconWidth}
            height={iconHeight}
            viewBox="0 0 128 128"
          >
            <path
              fill="#cecece"
              d="M64.347 41.619v4.292H44.872l-.029-.028l-.028.027H6.696a.07.07 0 0 0-.07.07v18.955H.5v.417h6.127v18.717a.07.07 0 0 0 .07.069h18.836v8.54h.417v-8.54h18.685v.07h.11l.097.097l.101-.097h.109v-.07h19.295v3.046h.416v-3.046H84.14v.07h.109l.1.097l.097-.097h.11v-.07h18.675v4.155h.416v-4.155h18.85a.07.07 0 0 0 .069-.07V65.353h4.934v-.417h-4.934V45.98a.07.07 0 0 0-.07-.07h-18.849v-.013h-.416v.014H84.378l-.028-.028l-.029.027H64.764v-4.29zm-57.484 4.43h18.67v18.71zm19.087 0h18.685v.04L25.95 64.747zm19.102 0h19.295v18.706l-19.295-18.67zm19.712 0h19.377v.036l-19.377 18.75zm19.793 0h18.674v18.685L84.557 46.09zm19.09 0h18.682L103.647 64.77zm-96.882.099l18.747 18.787H6.765zm115.66 0v18.787h-18.747zm-77.375.13l19.28 18.657H45.05zm39.088 0v18.657h-19.28zm-39.505.008v18.648H25.956zm39.922 0l18.674 18.645v.004H84.555zM6.764 65.351h18.578L6.764 83.901zm19.359 0h18.51v18.55zm18.927 0h19.178L45.05 83.91zm19.911 0h19.178V83.91zm19.595 0h18.51l-18.51 18.55zm19.09 0h.004L122.326 84h-18.681zm.201 0h18.578v18.55zm-39.085.001L84.032 84h-19.27zm-39.23.006v18.64H6.863zm.417.014l18.588 18.626H25.949zm77.28.012v18.615H84.655zm-38.883.047v18.567H45.158z"
            />
            <path
              fill="#6c6c6c"
              d="M64.556 51.492a1.41 1.41 0 0 0-1.052 2.343L29.677 73.063l.036.061c2.157 3.643 4.791 6.984 8.055 9.924l.052.047l.046-.053l25.746-29.097a1.41 1.41 0 1 0 .945-2.452zm0 .138a1.27 1.27 0 1 1-.898 2.169a1.27 1.27 0 0 1 .898-2.169zm48.339.426v.14h1.55v30.91h-1.55v.14h3.239v-.14h-1.55v-30.91h1.55v-.14zm-93.671.513l-.07.003h-.002a5.528 5.528 0 0 0-.071.004l-.065.004v4.114l.076-.008a.644.644 0 1 1 0 1.284l-.076-.008v4.116l.066.003l.07.002h.003a4.752 4.752 0 0 0 .07-9.504zm-.068.142a4.615 4.615 0 0 1 4.615 4.617a4.615 4.615 0 0 1-4.616 4.616v-3.832a.785.785 0 0 0 0-1.569v-3.832zm59.98.192v.003a2.56 2.56 0 0 0 0 5.117V71.62h-.006a2.563 2.563 0 0 0 0 5.125a2.561 2.561 0 0 0 .145-5.117V58.022c1.381-.037 2.492-1.167 2.492-2.558s-1.11-2.522-2.492-2.559v-.003zm0 .142v4.84a2.42 2.42 0 0 1 0-4.84zm.139 0a2.42 2.42 0 0 1 0 4.84zm-16.016 1.09L37.81 82.895c-3.21-2.902-5.808-6.194-7.94-9.783zm-31.086.853v3.239h.138v-1.55h6.565v1.55h.14v-3.239h-.14v1.55h-6.565v-1.55zm24.894 12.705v.139h1.55V77.9h-1.55v.139h3.238v-.14h-1.55V67.833h1.55v-.139zm22.063 4.065h.006v4.846h-.006a2.422 2.422 0 0 1-2.424-2.423a2.422 2.422 0 0 1 2.424-2.423zm.144.007a2.42 2.42 0 0 1 0 4.832zm13.243.435v3.24h.14v-1.55h12.022v1.55h.14V72.2h-.14v1.55H92.656V72.2z"
            />
            <path
              fill="#7f2d2d"
              d="m81.067 45.112l-.297.001c-1.515.024-4.762.018-7.67 1.334c-2.907 1.316-5.463 4.044-5.463 9.248c0 2.2.734 4.1 1.886 5.73h-23.21V50.914H61.55v-5.351H40.185v5.35h.002v10.512h-.002v5.35h.002v12.457l-3.58-.022l-4.954.023l-7.755-12.048c1.818-.75 3.597-1.828 4.966-3.339c1.49-1.643 2.486-3.79 2.486-6.447v-.764c0-3.887-1.482-6.676-3.9-8.454c-2.417-1.778-5.724-2.564-9.4-2.647H6.25v5.41h.03v12.709h-.03v5.051h.03v15.854h6.126v-15.87l6.16-.017l8.457 13.759l.012.016c.717.948 2.205 3.054 4.61 4.57l.205.13l4.861-2.565l3.894-.023h20.944v-5.561H46.312V66.775H76.44l.031.015c1.867.853 4.132 1.625 5.896 2.738c1.763 1.112 2.997 2.489 2.997 4.675c0 2.354-1.062 3.586-2.56 4.334s-3.453.933-5.063.933h-.003c-3.087.019-6.718-1.293-9.819-2.328l-.548-.183v5.883l.243.111c3.044 1.388 7.552 1.93 10.135 1.831c1.854 0 5.238-.364 8.225-1.859c2.992-1.497 5.585-4.21 5.585-8.722c0-3.492-1.314-5.996-3.153-7.788c-1.84-1.792-4.183-2.89-6.276-3.706c-.795-.307-2.3-.908-3.797-1.723c-1.494-.813-2.972-1.853-3.71-2.944c-.46-.746-.743-1.576-.792-2.361c.004-2.38 1.113-3.663 2.55-4.42c1.438-.758 3.23-.92 4.401-.835c2.355.17 6.413 1.5 7.711 2.053l.413.177l.6-1.765h16.245v33.667h6.126V50.89h11.01v-5.304h-11.01v-.024h-6.126v.024H84.585c-1.176-.284-2.357-.465-3.519-.476zm-.008.833c1.1.01 2.241.183 3.39.464l.049.012h22.089v-.024h4.46v.024h11.01v3.637h-11.01v33.667h-4.46V50.058H88.913l-.51 1.497c-1.637-.65-5.154-1.786-7.558-1.96c-1.3-.093-3.208.064-4.85.93c-1.643.865-2.996 2.51-2.996 5.17v.025c.058.954.394 1.914.923 2.77l.004.007l.005.007c.882 1.308 2.455 2.37 4.007 3.215c1.551.844 3.089 1.457 3.894 1.767c2.05.8 4.288 1.864 5.994 3.527c1.707 1.663 2.902 3.904 2.902 7.19c0 4.2-2.312 6.57-5.124 7.978c-2.812 1.407-6.122 1.771-7.86 1.771h-.017c-2.357.091-6.68-.442-9.52-1.66v-4.175c2.968 1.001 6.405 2.206 9.539 2.187c1.67 0 3.732-.171 5.434-1.021c1.702-.85 3.02-2.46 3.02-5.08c0-2.509-1.5-4.19-3.386-5.38c-1.887-1.19-4.189-1.965-5.994-2.79l-.11-.052l-.083-.038H45.48V79.83h15.237v3.894H40.603l-4.1.024l-4.606 2.43c-2.117-1.397-3.468-3.27-4.185-4.22l-8.68-14.122l-7.46.02v15.868H7.115V67.871h-.03v-3.385h.03V50.111h-.03v-3.744h10.948c3.567.081 6.707.854 8.925 2.485c2.219 1.632 3.561 4.103 3.561 7.783v.764c0 2.45-.898 4.373-2.27 5.888c-1.373 1.514-3.232 2.61-5.12 3.324l-.48.182c2.863 4.417 5.704 8.849 8.552 13.275l5.407-.025l4.414.026V65.942h-.002v-3.684h.002V50.08h-.002v-3.684h19.7v3.684H45.48v12.178h25.726l-.559-.681c-1.348-1.643-2.176-3.578-2.176-5.882c0-4.94 2.281-7.27 4.974-8.49c2.692-1.218 5.807-1.235 7.34-1.259c.091-.001.183-.002.275 0zm-69.487 4.167v14.375h5.057c2.126 0 4.361-.312 6.113-1.367c1.751-1.055 2.973-2.9 2.973-5.72v-.764c0-2.855-1.603-4.554-3.336-5.451c-1.732-.898-3.578-1.073-4.339-1.073zm.834.833h5.634c.62 0 2.405.175 3.956.979c1.551.804 2.886 2.159 2.886 4.712v.764c0 2.588-1.029 4.077-2.57 5.006s-3.641 1.247-5.683 1.247h-4.223z"
            />
            <path
              fill="#212121"
              d="M12.074 28.415a.139.139 0 0 0-.139.139v2.744c0 .148.01.334.027.561c.007.096.015.15.022.229c-.109-.125-.208-.257-.344-.361a2.55 2.55 0 0 0-.776-.41a3.265 3.265 0 0 0-1.043-.151c-.933 0-1.702.32-2.27.952c-.573.634-.85 1.562-.85 2.762c0 1.188.27 2.106.83 2.731c.56.622 1.33.934 2.27.934c.402 0 .754-.05 1.056-.151a.139.139 0 0 0 .001 0c.302-.105.564-.245.783-.423c.154-.122.265-.267.381-.409l.125.742a.139.139 0 0 0 .137.116h.88a.139.139 0 0 0 .14-.139v-9.727a.139.139 0 0 0-.14-.139zm4.115.313a.837.837 0 0 0-.565.203c-.16.142-.23.36-.23.617c0 .254.07.47.228.615a.139.139 0 0 0 .002.001a.837.837 0 0 0 .565.204c.208 0 .4-.07.55-.203c.167-.143.245-.362.245-.617c0-.259-.078-.479-.246-.618a.82.82 0 0 0-.55-.202zm21.769 2.297c-.593 0-1.105.094-1.535.288c-.429.193-.764.48-.994.853c-.23.371-.342.818-.342 1.33c0 .486.123.922.37 1.296a.139.139 0 0 0 .002.001c.203.297.471.509.774.668c-.215.144-.4.294-.526.456a1.194 1.194 0 0 0-.246.742c0 .245.077.471.227.661a.139.139 0 0 0 .001.002c.079.097.168.18.265.252c-.383.119-.721.287-.967.546a.139.139 0 0 0-.001 0a1.704 1.704 0 0 0-.464 1.196c0 .643.287 1.168.83 1.522h.001c.545.36 1.301.53 2.263.53c1.241 0 2.203-.203 2.885-.628c.68-.425 1.037-1.064 1.037-1.862c0-.632-.232-1.142-.686-1.48c-.45-.338-1.081-.496-1.883-.496h-1.268a2.82 2.82 0 0 1-.554-.047a.698.698 0 0 1-.31-.142c-.054-.052-.08-.113-.08-.216c0-.15.042-.274.133-.388a1.42 1.42 0 0 1 .424-.32c.195.028.389.046.578.046c.871 0 1.575-.206 2.091-.632c.516-.429.78-1.022.78-1.738c0-.294-.046-.566-.14-.813c-.063-.163-.153-.29-.238-.424l1.122-.132a.139.139 0 0 0 .123-.138v-.669a.139.139 0 0 0-.139-.139h-2.457a2.455 2.455 0 0 0-.3-.06a3.545 3.545 0 0 0-.386-.046h-.001a4.02 4.02 0 0 0-.39-.019zm-15.918.025c-.476 0-.93.058-1.363.174a6.324 6.324 0 0 0-1.141.416a.139.139 0 0 0-.067.179l.335.787a.139.139 0 0 0 .186.072c.3-.139.618-.26.954-.362c.328-.1.673-.15 1.037-.15c.463 0 .801.111 1.037.32c.224.2.354.57.354 1.141v.286l-1.108.044c-1.178.034-2.067.233-2.67.622c-.602.388-.918.97-.918 1.693c0 .473.101.877.312 1.2a.139.139 0 0 0 0 .002c.212.317.503.557.862.713a.139.139 0 0 0 .001 0c.361.155.77.23 1.224.23c.425 0 .787-.042 1.09-.13c.304-.093.573-.227.806-.405a.139.139 0 0 0 .002 0c.176-.138.34-.32.504-.505l.168.805a.139.139 0 0 0 .135.11h.795a.139.139 0 0 0 .14-.139v-4.657c0-.828-.218-1.46-.672-1.86c-.451-.399-1.125-.586-2.003-.586zm8.374.116c-.337 0-.659.045-.965.137a2.742 2.742 0 0 0-.836.394a2.22 2.22 0 0 0-.468.45l-.123-.74a.139.139 0 0 0-.137-.116h-.88a.139.139 0 0 0-.139.139v6.851a.139.139 0 0 0 .139.14h1.09a.139.139 0 0 0 .14-.14v-3.588c0-.799.159-1.39.457-1.785c.291-.386.799-.59 1.57-.59c.542 0 .916.134 1.155.383c.244.25.375.637.375 1.185v4.395a.139.139 0 0 0 .139.14h1.077a.139.139 0 0 0 .139-.14v-4.463c0-.902-.227-1.585-.702-2.016c-.471-.43-1.156-.636-2.031-.636zm15.529.013c-.707 0-1.325.144-1.848.436c-.519.288-.92.714-1.199 1.265c-.28.549-.416 1.21-.416 1.976c0 .575.08 1.094.245 1.553a.139.139 0 0 0 0 .001c.168.457.403.848.706 1.167a.139.139 0 0 0 .001 0c.307.318.67.564 1.085.733a.139.139 0 0 0 .002.001c.42.165.88.247 1.378.247c.53 0 1.01-.081 1.436-.247c.43-.17.798-.415 1.1-.734c.304-.32.536-.711.695-1.169c.16-.46.237-.977.237-1.552c0-.763-.14-1.422-.43-1.971a2.994 2.994 0 0 0-1.203-1.27c-.514-.292-1.113-.436-1.79-.436zm-30.312.112a.139.139 0 0 0-.14.139v7.958c0 .396-.089.638-.227.757c-.156.134-.359.204-.632.204c-.168 0-.318-.012-.448-.035a.139.139 0 0 0-.004-.001a2.683 2.683 0 0 1-.394-.09a.139.139 0 0 0-.18.134v.844a.139.139 0 0 0 .095.131c.13.044.282.081.453.111c.177.036.38.053.61.053c.463 0 .854-.082 1.17-.255a1.62 1.62 0 0 0 .702-.75c.151-.319.224-.696.224-1.128V31.43a.139.139 0 0 0-.14-.139zm22.288.78c.498 0 .85.122 1.085.35c.234.222.358.561.358 1.05c0 .454-.12.774-.35.993c-.23.219-.582.337-1.08.337c-.48 0-.829-.117-1.069-.338c-.24-.221-.362-.533-.362-.973c0-.484.124-.827.359-1.058c.241-.237.584-.36 1.059-.36zm-27.946.235c.774 0 1.266.217 1.538.637c.285.434.438 1.077.438 1.931v.188c0 .803-.158 1.39-.45 1.772c-.288.374-.78.57-1.526.57c-.643 0-1.091-.207-1.398-.629c-.305-.426-.467-1.046-.467-1.87c0-.827.164-1.465.475-1.922c.31-.456.754-.677 1.39-.677zm35.944.025c.488 0 .872.104 1.163.301c.296.2.513.483.658.86a.139.139 0 0 0 0 .001c.145.376.22.83.22 1.363c0 .537-.075.997-.22 1.382a1.777 1.777 0 0 1-.665.872c-.292.203-.67.307-1.15.307c-.483 0-.864-.105-1.156-.306a1.792 1.792 0 0 1-.658-.873c-.146-.385-.22-.845-.22-1.382c0-.814.168-1.435.49-1.874h.001v-.001c.322-.432.817-.65 1.537-.65zm-22.558 2.59v.488c0 .647-.189 1.103-.561 1.412c-.38.315-.866.474-1.481.474c-.39 0-.688-.087-.908-.253c-.213-.16-.32-.396-.32-.758c0-.412.155-.704.49-.929c.328-.218.941-.362 1.827-.395zm13.988 3.227h1.248c.361 0 .664.025.905.073a.139.139 0 0 0 .002 0c.234.042.396.123.502.234c.1.109.16.277.16.53a.935.935 0 0 1-.259.668a.139.139 0 0 0-.002.002c-.17.19-.438.345-.815.453a.139.139 0 0 0-.001 0c-.371.111-.852.17-1.438.17c-.594 0-1.039-.099-1.335-.275c-.295-.173-.424-.395-.424-.725c0-.257.057-.46.166-.621c.114-.164.275-.287.495-.375a2.14 2.14 0 0 1 .796-.134zm18.12 51.362c-.507 0-.945.088-1.31.271a1.863 1.863 0 0 0-.844.862c-.193.386-.284.873-.284 1.463v.35l-1.171.316a.139.139 0 0 0-.103.134v.5a.139.139 0 0 0 .139.139h1.135v5.9a.139.139 0 0 0 .139.139h1.09a.139.139 0 0 0 .14-.14v-5.9h1.653a.139.139 0 0 0 .139-.138v-.813a.139.139 0 0 0-.139-.139h-1.654v-.36c0-.53.099-.9.266-1.116c.173-.222.43-.334.817-.334c.183 0 .36.02.534.059a.139.139 0 0 0 .003 0c.185.038.35.078.492.123a.139.139 0 0 0 .173-.088l.282-.819a.139.139 0 0 0-.087-.177a5.17 5.17 0 0 0-.628-.16a3.973 3.973 0 0 0-.782-.072zm61.107.069a.139.139 0 0 0-.14.139v9.727a.139.139 0 0 0 .14.139h1.084a.139.139 0 0 0 .138-.14v-2.418l.716-.625l2.451 3.13a.139.139 0 0 0 .11.053h1.313a.139.139 0 0 0 .11-.225l-3.031-3.83l2.81-2.838a.139.139 0 0 0-.099-.237h-1.28a.139.139 0 0 0-.1.042l-2.39 2.425a.139.139 0 0 0-.002.002c-.126.133-.278.305-.46.519a.139.139 0 0 0 0 .001l-.182.219l.014-.273c.013-.244.02-.45.02-.62v-5.051a.139.139 0 0 0-.139-.14zM86.657 92.2c-.665 0-1.253.152-1.754.458a3.075 3.075 0 0 0-1.156 1.309c-.27.56-.402 1.219-.402 1.973c0 .772.146 1.434.444 1.98c.297.542.717.96 1.253 1.244c.54.279 1.168.416 1.877.416a6.65 6.65 0 0 0 1.288-.11c.37-.072.74-.188 1.111-.345a.139.139 0 0 0 .085-.128v-.913a.139.139 0 0 0-.192-.128a6.78 6.78 0 0 1-1.068.343a5.38 5.38 0 0 1-1.178.115c-.713 0-1.243-.198-1.62-.589c-.353-.364-.546-.897-.58-1.602h4.82a.139.139 0 0 0 .14-.14v-.643c0-.638-.12-1.203-.363-1.688a2.7 2.7 0 0 0-1.059-1.145c-.462-.272-1.014-.407-1.646-.407zm18.799 0c-.707 0-1.325.144-1.848.437a2.915 2.915 0 0 0-1.2 1.265c-.278.549-.415 1.21-.415 1.976c0 .575.081 1.094.245 1.553a.139.139 0 0 0 0 .001c.168.457.403.847.706 1.167a.139.139 0 0 0 .001 0c.307.318.67.563 1.085.733a.139.139 0 0 0 .002 0c.42.166.881.248 1.378.248c.53 0 1.01-.082 1.436-.247c.43-.17.798-.415 1.101-.734c.304-.32.535-.711.694-1.17a4.72 4.72 0 0 0 .238-1.551c0-.763-.142-1.422-.43-1.971a2.994 2.994 0 0 0-1.204-1.27c-.513-.292-1.113-.436-1.789-.436zm-39.097.013c-.476 0-.93.058-1.363.173a6.324 6.324 0 0 0-1.142.416a.139.139 0 0 0-.066.18l.335.787a.139.139 0 0 0 .186.072c.3-.14.618-.26.954-.363c.327-.1.673-.15 1.036-.15c.464 0 .802.112 1.038.322c.224.2.354.569.354 1.14v.285l-1.108.045h.001c-1.178.033-2.068.233-2.672.622c-.602.388-.917.97-.917 1.692c0 .474.1.878.311 1.2a.139.139 0 0 0 .001.002c.212.318.502.558.862.713c.362.155.77.23 1.224.23c.425 0 .788-.042 1.09-.13c.304-.092.574-.227.807-.404a.139.139 0 0 0 .001-.001c.177-.138.341-.32.505-.505l.167.805a.139.139 0 0 0 .136.11h.795a.139.139 0 0 0 .138-.138v-4.658c0-.828-.217-1.46-.67-1.86c-.452-.398-1.125-.585-2.003-.585zm-5.163.115c-.358 0-.69.066-.989.2c-.29.132-.548.31-.77.534c-.147.146-.258.318-.376.485l-.09-.968a.139.139 0 0 0-.139-.126h-.906a.139.139 0 0 0-.14.14v6.85a.139.139 0 0 0 .14.14h1.096a.139.139 0 0 0 .14-.14V95.77c0-.34.052-.643.155-.913a2.05 2.05 0 0 1 .424-.698a.139.139 0 0 0 .001-.002c.18-.194.386-.34.622-.441a.139.139 0 0 0 .001 0c.241-.105.495-.158.766-.158a3.43 3.43 0 0 1 .768.09a.139.139 0 0 0 .17-.115l.139-.963a.139.139 0 0 0-.11-.156a3.643 3.643 0 0 0-.437-.058a4.452 4.452 0 0 0-.465-.026zm13.272 0c-.319 0-.622.044-.907.131a2.552 2.552 0 0 0-.778.39a2.216 2.216 0 0 0-.428.435l-.12-.715a.139.139 0 0 0-.138-.116h-.88a.139.139 0 0 0-.139.14v6.85a.139.139 0 0 0 .14.14h1.09a.139.139 0 0 0 .138-.14V95.82c0-.526.063-.963.183-1.31v-.001c.123-.347.313-.597.575-.767c.26-.168.615-.259 1.074-.259c.32 0 .573.06.765.17a.139.139 0 0 0 .003.001c.197.107.34.263.438.484a.139.139 0 0 0 .001.002c.103.222.158.51.158.867v4.439a.139.139 0 0 0 .139.139h1.084a.139.139 0 0 0 .138-.14v-3.832c0-.726.154-1.256.442-1.605c.283-.345.739-.525 1.41-.525c.468 0 .793.128 1.013.373a.139.139 0 0 0 .001.001c.223.241.344.617.344 1.15v4.439a.139.139 0 0 0 .14.139h1.076a.139.139 0 0 0 .14-.14v-4.488c0-.892-.207-1.565-.647-1.993c-.435-.428-1.074-.634-1.89-.634c-.508 0-.98.102-1.411.307h-.001c-.387.18-.692.463-.933.814a1.828 1.828 0 0 0-.783-.811c-.393-.209-.873-.31-1.437-.31zm39.352 0c-.358 0-.69.066-.989.2c-.29.132-.548.31-.77.534c-.147.146-.258.318-.376.485l-.09-.968a.139.139 0 0 0-.139-.126h-.906a.139.139 0 0 0-.14.14v6.85a.139.139 0 0 0 .14.14h1.096a.139.139 0 0 0 .14-.14V95.77c0-.34.052-.643.155-.913c.104-.278.245-.509.424-.698a.139.139 0 0 0 0-.002a1.8 1.8 0 0 1 .623-.441a.139.139 0 0 0 .001 0a1.89 1.89 0 0 1 .766-.158a3.425 3.425 0 0 1 .768.09a.139.139 0 0 0 .17-.115l.139-.963a.139.139 0 0 0-.11-.156a3.643 3.643 0 0 0-.437-.058a4.451 4.451 0 0 0-.465-.026zm-22.946.126a.139.139 0 0 0-.133.177l1.984 6.852a.139.139 0 0 0 .133.1h1.228a.139.139 0 0 0 .132-.094l1.339-3.968a8.57 8.57 0 0 0 .167-.514a.139.139 0 0 0 0-.001c.048-.171.092-.333.131-.488l.001-.003c.03-.104.052-.195.076-.288c.024.093.049.183.075.288a.139.139 0 0 0 .002.004l.138.475a.139.139 0 0 0 .001.004l.164.501l1.28 3.988a.139.139 0 0 0 .133.096h1.267a.139.139 0 0 0 .134-.1l1.99-6.852a.139.139 0 0 0-.133-.177h-1.11a.139.139 0 0 0-.134.101l-1.05 3.783a.139.139 0 0 0-.001 0l-.204.764a.139.139 0 0 0 0 .002c-.06.243-.113.464-.16.668a15.612 15.612 0 0 0-.176-.629l-.001-.002a15.861 15.861 0 0 0-.192-.628l-1.28-3.963a.139.139 0 0 0-.132-.096h-1.176a.139.139 0 0 0-.132.095l-1.326 3.97a16.575 16.575 0 0 0-.285.971a.139.139 0 0 0-.001.002l-.077.32l-.007-.036c-.045-.219-.1-.449-.165-.691l-.001-.003a26.786 26.786 0 0 0-.197-.744l-1.038-3.782a.139.139 0 0 0-.134-.102zm-4.23.874c.392 0 .7.083.934.24a.139.139 0 0 0 .001 0c.24.156.415.372.532.661a.139.139 0 0 0 .001.003c.107.251.162.55.18.881h-3.484c.08-.544.253-.98.544-1.284c.319-.335.738-.5 1.292-.5zm18.786.025c.488 0 .872.104 1.163.301c.295.2.513.483.657.86c.146.377.221.83.221 1.364c0 .537-.075.997-.22 1.382a1.776 1.776 0 0 1-.665.872c-.293.202-.671.307-1.15.307c-.483 0-.864-.105-1.156-.307a1.792 1.792 0 0 1-.658-.872c-.146-.385-.221-.845-.221-1.382c0-.814.169-1.435.491-1.874l.001-.001c.322-.432.817-.65 1.537-.65zm-37.751 2.731v.487c0 .648-.189 1.104-.561 1.412c-.38.315-.866.475-1.481.475c-.39 0-.688-.088-.908-.253c-.213-.16-.32-.396-.32-.758c0-.413.155-.705.49-.93c.328-.218.941-.361 1.827-.394z"
            />
          </svg>
        </div>
      </nav>
      <aside>
        <p>Copyright © {new Date().getFullYear()} - Made by Shebeli</p>
      </aside>
    </footer>
  );
}
